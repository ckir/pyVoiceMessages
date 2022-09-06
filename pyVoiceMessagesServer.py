import asyncio
from aiorun import run
import json
import datetime
import argparse
import sys
import os
import pyttsx3
from colorama import init, Fore, Back, Style
init()
print(Style.RESET_ALL)

try:
    engine = pyttsx3.init()
except Exception as e:
    print("Failed to load pyttsx3. Does your system have audio capabilities?")
    sys.exit(1)
background_tasks = set()
available_voices = {}
verbose_mode = False
if sys.platform == 'darwin':
    default_voice = int(os.getenv("PYVOICEMESSAGESVOICE", "0"))
elif sys.platform == 'win32':
    default_voice = int(os.getenv("PYVOICEMESSAGESVOICE", "0"))
else:
    default_voice = int(os.getenv("PYVOICEMESSAGESVOICE", "12"))

async def voice_message(message):
    print(Fore.MAGENTA + "{ts} Just said: '{m}'".format(ts = datetime.datetime.now().isoformat(), m=message['message']))
    # Without the "Warning! " addition the pyttsx3 truncates the message !!!
    try:
        engine.setProperty('voice', available_voices[message["voice"]]["voice_id"])
    except Exception:
        print("Voice", message["voice"], "is not available")
        engine.setProperty('voice', available_voices[default_voice]["voice_id"])

    engine.say("Warning! " + message['message'])
    engine.runAndWait()
    # await asyncio.sleep(3600)


async def voice_message_repeat(message):
    for i in range(0, message['repeat']):
        await voice_message(message)
        if i < message['repeat']:
            await asyncio.sleep(message['interval'])


async def handle_request(reader, writer):
    try:
        data = await reader.read(8192)
        message = data.decode()
        message = json.loads(str(message))
        pending_tasks = asyncio.all_tasks()
        pending_tasks_names = []
        for penging_task in pending_tasks:
            pending_tasks_names.append(penging_task.get_name())
        if message["switch"] == "on":
            if message['message'] not in pending_tasks_names:
                resp = {
                    "ts": datetime.datetime.now().isoformat(),
                    "response": "Message '{m}' NOT exists. Created".format(m=message['message'])
                }
                resp = json.dumps(resp)
                writer.write(resp.encode())
                await writer.drain()

                new_message = asyncio.create_task(
                    voice_message_repeat(message), name=message['message']
                )
                background_tasks.add(new_message)
                new_message.add_done_callback(background_tasks.discard)
                print(Fore.GREEN + "{ts} Created message '{m}'".format(ts = datetime.datetime.now().isoformat(), m=message['message']))
                await new_message
            else:
                msg = "Message '{m}' already exists. Ignoring".format(m=message['message'])
                resp = {
                    "ts": datetime.datetime.now().isoformat(),
                    "response": msg
                }
                resp = json.dumps(resp)
                writer.write(resp.encode())
                if verbose_mode:
                    print(Fore.MAGENTA + datetime.datetime.now().isoformat(), msg)
                await writer.drain()
        if message["switch"] == "off":
            if message['message'] in pending_tasks_names:
                for task in asyncio.all_tasks():
                    if message['message'] == task.get_name():
                        resp = {
                            "ts": datetime.datetime.now().isoformat(),
                            "response": "Message '{m}' canceled".format(m=message['message'])
                        }
                        resp = json.dumps(resp)
                        writer.write(resp.encode())
                        writer.write(data)
                        await writer.drain()
                        task.add_done_callback(background_tasks.discard)
                        print(Fore.YELLOW + "{ts} Canceled message '{m}'".format(ts = datetime.datetime.now().isoformat(), m=message['message']))
                        task.cancel()
            else:
                resp = {
                        "ts": datetime.datetime.now().isoformat(),
                        "response": "Message '{m}' not found".format(m=message['message'])
                        }
                resp = json.dumps(resp)
                writer.write(resp.encode())
                writer.write(data)
                print( Fore.WHITE + datetime.datetime.now().isoformat(), "Message '{m}' not found".format(m=message['message']))
                await writer.drain()
        writer.close()
    except Exception as e:
        print( Fore.RED + datetime.datetime.now().isoformat(), str(e))

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, nargs='?', default=8888)
    parser.add_argument('-V', '--verbose',
                    default=False,
                    action=argparse.BooleanOptionalAction,
                    dest='verbose',
                    help='Prints the server response'
                    )
    args = parser.parse_args()
    print("Available voices:")
    voices = engine.getProperty('voices')
    v = 0
    for voice in voices:
        vn = str(voice.name)
        vi = str(voice.id)
        available_voices[v] = {"voice_name": vn, "voice_id": voice.id }
        print(v, voice.name, "(", voice.id, ")")
        v = v + 1
    print()
    print("Speaking ", available_voices[default_voice]["voice_name"], " (", available_voices[default_voice]["voice_id"], ")")
    server = await asyncio.start_server(handle_request, '127.0.0.1', args.port)
    try:
        engine.setProperty('voice', available_voices[default_voice]["voice_id"])
    except Exception:
        print("Voice", default_voice, "is not available")
        sys.exit(1)
    started_message = 'Serving on {}'.format(server.sockets[0].getsockname())
    engine.say("Warning! " + started_message)
    engine.runAndWait()
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        while True:
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        server.close()
        await server.wait_closed()

run(main())
print(Style.RESET_ALL)

