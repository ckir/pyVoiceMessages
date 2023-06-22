import sys
from colorama import init, Fore, Back, Style
from tendo import singleton
try:
    me = singleton.SingleInstance()
except singleton.SingleInstanceException as e:
    sys.exit(-1)

import asyncio
from aiorun import run
import json
import datetime
import argparse

import os
import pyttsx3


init()
print(Style.RESET_ALL)


try:
    engine = pyttsx3.init()
except Exception as e:
    print(
        Fore.RED
        + "Failed to load pyttsx3. Does your system have audio capabilities?"
        + Fore.RESET_ALL
    )
    sys.exit(1)
background_tasks = set()
available_voices = {}
verbose_mode = False
if sys.platform == "darwin":
    default_voice = int(os.getenv("PYVOICEMESSAGESVOICE", "0"))
elif sys.platform == "win32":
    default_voice = int(os.getenv("PYVOICEMESSAGESVOICE", "0"))
else:
    default_voice = int(os.getenv("PYVOICEMESSAGESVOICE", "12"))


def get_voices():
    available = {}
    voices = engine.getProperty("voices")
    voices = [vars(voice) for voice in voices]
    v = 0
    for voice in voices:
        voice["languages"] = list(map(lambda x: x.decode("utf-8"), voice["languages"]))
        available[v] = voice
        v = v + 1
    return available


get_voices()


async def voice_message(message):
    print(
        Fore.MAGENTA
        + "{ts} Just said: '{m}'".format(
            ts=datetime.datetime.now().isoformat(), m=message["message"]
        )
    )
    # Without the "Warning! " addition the pyttsx3 truncates the message !!!
    try:
        engine.setProperty("voice", available_voices[message["voice"]]["voice_id"])
    except Exception:
        if verbose_mode:
            print("Voice", message["voice"], "is not available")
        engine.setProperty("voice", available_voices[default_voice]["voice_id"])

    engine.say(message["message"])
    engine.runAndWait()
    # await asyncio.sleep(3600)


async def voice_message_repeat(message):
    for i in range(0, message["repeat"]):
        await voice_message(message)
        if i < message["repeat"]:
            await asyncio.sleep(message["interval"])


async def handle_request(reader, writer):
    try:
        data = await reader.read(8192)
        message = data.decode()
        message = json.loads(str(message))
        if message["command"] == "list":
            resp = {
                "ts": datetime.datetime.now().isoformat(),
                "type": "list",
                "response": get_voices(),
            }
            resp = json.dumps(resp) + '<EOF>'
            writer.write(resp.encode())
            await writer.drain()
        else:
            pending_tasks = asyncio.all_tasks()
            pending_tasks_names = []
            for penging_task in pending_tasks:
                pending_tasks_names.append(penging_task.get_name())
            if message["command"] == "on":
                if message["message"] not in pending_tasks_names:
                    resp = {
                        "ts": datetime.datetime.now().isoformat(),
                        "type": "message",
                        "response": "Message '{m}' NOT exists. Created".format(
                            m=message["message"]
                        ),
                    }
                    resp = json.dumps(resp) + '<EOF>'
                    writer.write(resp.encode())
                    await writer.drain()

                    new_message = asyncio.create_task(
                        voice_message_repeat(message), name=message["message"]
                    )
                    background_tasks.add(new_message)
                    new_message.add_done_callback(background_tasks.discard)
                    if verbose_mode:
                        print(
                            Fore.GREEN
                            + "{ts} Created message '{m}'".format(
                                ts=datetime.datetime.now().isoformat(),
                                m=message["message"],
                            )
                        )
                    await new_message
                else:
                    msg = "Message '{m}' already exists. Ignoring".format(
                        m=message["message"]
                    )
                    resp = {"ts": datetime.datetime.now().isoformat(), "response": msg}
                    resp = json.dumps(resp) + '<EOF>'
                    writer.write(resp.encode())
                    if verbose_mode:
                        print(Fore.MAGENTA + datetime.datetime.now().isoformat(), msg)
                    await writer.drain()
            if message["command"] == "off":
                if message["message"] in pending_tasks_names:
                    for task in asyncio.all_tasks():
                        if message["message"] == task.get_name():
                            resp = {
                                "ts": datetime.datetime.now().isoformat(),
                                "type": "message",
                                "response": "Message '{m}' canceled".format(
                                    m=message["message"]
                                ),
                            }
                            resp = json.dumps(resp)  + '<EOF>'
                            writer.write(resp.encode())
                            writer.write(data)
                            await writer.drain()
                            task.add_done_callback(background_tasks.discard)
                            if verbose_mode:
                                print(
                                    Fore.YELLOW
                                    + "{ts} Canceled message '{m}'".format(
                                        ts=datetime.datetime.now().isoformat(),
                                        m=message["message"],
                                    )
                                )
                            task.cancel()
                else:
                    resp = {
                        "ts": datetime.datetime.now().isoformat(),
                        "type": "error",
                        "response": "Message '{m}' not found".format(
                            m=message["message"]
                        ),
                    }
                    resp = json.dumps(resp) + '<EOF>'
                    writer.write(resp.encode())
                    writer.write(data)
                    if verbose_mode:
                        print(
                            Fore.WHITE + datetime.datetime.now().isoformat(),
                            "Message '{m}' not found".format(m=message["message"]),
                        )
                    await writer.drain()
            writer.close()
    except Exception as e:
        print(Fore.RED + datetime.datetime.now().isoformat(), str(e))


async def main(args):
    print("Available voices:")
    voices = engine.getProperty("voices")
    v = 0
    for voice in voices:
        vn = str(voice.name)
        vi = str(voice.id)
        available_voices[v] = {"voice_name": vn, "voice_id": voice.id}
        print(v, voice.name, "(", voice.id, ")")
        v = v + 1
    print()
    print(
        "Speaking ",
        available_voices[default_voice]["voice_name"],
        " (",
        available_voices[default_voice]["voice_id"],
        ")",
    )
    if args.listonly:
        asyncio.get_event_loop().stop()
    server = await asyncio.start_server(handle_request, "0.0.0.0", args.port)
    try:
        engine.setProperty("voice", available_voices[default_voice]["voice_id"])
    except Exception:
        print("Voice", default_voice, "is not available")
        sys.exit(1)
    started_message = "Serving on port {}".format(args.port)
    engine.say(started_message)
    engine.runAndWait()
    print("Serving on {}".format(server.sockets[0].getsockname()))
    try:
        while True:
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "port",
        type=int,
        nargs="?",
        default=8888,
        help="Port to listen",
    )
    parser.add_argument(
        "-V",
        "--verbose",
        default=False,
        action=argparse.BooleanOptionalAction,
        dest="verbose",
        help="Prints server activity messages",
    )
    parser.add_argument(
        "-L",
        "--list",
        default=False,
        action=argparse.BooleanOptionalAction,
        dest="listonly",
        help="List available voices and exit",
    )
    args = parser.parse_args()
    try:
        run(
            main(args),
            stop_on_unhandled_errors=True,
        )
    except Exception as error:
        print(Style.RESET_ALL)
