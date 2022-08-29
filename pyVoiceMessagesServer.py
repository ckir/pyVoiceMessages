import asyncio
from aiorun import run
import json
import datetime
import argparse
import pyttsx3

engine = pyttsx3.init()
background_tasks = set()
available_voices = {}
verbose_mode = False


async def voice_message(message):
    print("{ts} Just said: '{m}'".format(ts = datetime.datetime.now().isoformat(), m=message['message']))
    # Without the "Warning! " addition the pyttsx3 truncates the message !!!
    engine.setProperty('voice', available_voices[message["voice"]]["voice_id"])
    engine.say("Warning! " + message['message'])
    engine.runAndWait()
    # await asyncio.sleep(3600)


async def voice_message_repeat(message):
    for i in range(0, message['repeat']):
        await voice_message(message)
        if i < message['repeat']:
            await asyncio.sleep(message['interval'])


async def handle_request(reader, writer):
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
            print("{ts} Created message '{m}'".format(ts = datetime.datetime.now().isoformat(), m=message['message']))
            await new_message
        else:
            msg = "Message '{m}' already exists. Ignoring".format(m=message['message'])
            resp = {
                "ts": datetime.datetime.now().isoformat(),
                "response": msg
            }
            resp = json.dumps(resp)
            writer.write(resp.encode())
            writer.write(resp)
            if verbose_mode:
                print(datetime.datetime.now().isoformat(), msg)
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
                    print("{ts} Canceled message '{m}'".format(ts = datetime.datetime.now().isoformat(), m=message['message']))
                    task.cancel()
        else:
            resp = {
                    "ts": datetime.datetime.now().isoformat(),
                    "response": "Message '{m}' not found".format(m=message['message'])
                    }
            resp = json.dumps(resp)
            writer.write(resp.encode())
            writer.write(data)
            print( "Message '{m}' not found".format(m=message['message']))
            await writer.drain()
    writer.close()


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
        available_voices[v] = {"voice_name": vn, "voice_id": vi}
        print(v, voice.name)
        v = v + 1
    server = await asyncio.start_server(handle_request, '127.0.0.1', args.port)
    engine.setProperty('voice', available_voices[1]["voice_id"])
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
