import asyncio
from aiorun import run
import json
import argparse
import datetime
from rich.console import Console
from rich.table import Table

async def tcp_echo_client(command, host, port, message, debug, outputjson):
    try:
        reader, writer = await asyncio.open_connection(
            host, port)

        writer.write(message.encode())

        data = await reader.read(8192)
        data = data.decode()
        if debug:
            print(datetime.datetime.now().isoformat(),
                  'Server said: %r' % data)

        writer.close()
        data = json.loads(data)
        if command == 'list':
            if outputjson:
                print(json.dumps(data['response'], indent=4))
            else:
                table = Table(title="Available Voices")
                table.add_column("#")
                for header in next (iter (data['response'].values ())).keys():
                    table.add_column(header.title())
                for voice in data['response']:
                    vdata = data['response'][voice]
                    if 'languages' in vdata and isinstance(vdata['languages'], list):
                        vdata['languages'] = ":".join(vdata['languages'])
                    row = list(vdata.values())
                    row.insert(0, voice)    
                    table.add_row(*row)
                console = Console()
                console.print(table)

    except Exception as e:
        print(datetime.datetime.now().isoformat(), repr(e))

    asyncio.get_event_loop().stop()


parser = argparse.ArgumentParser()
parser.add_argument('command',
                    choices=('on', 'off', 'list'),
                    help='on = create new message / off = cancel existing message / list = list server voices',
                    type=str
                    )
parser.add_argument('message',
                    help='Provide text to say',
                    type=str
                    )
parser.add_argument('-H', '--host',
                    default='localhost',
                    dest='host',
                    help='Provide destination host. Defaults to localhost',
                    type=str
                    )
parser.add_argument('-P', '--port',
                    default=8888,
                    dest='port',
                    help='Provide destination port. Defaults to 8888',
                    type=int
                    )
parser.add_argument('-R', '--repeat',
                    default=1,
                    dest='repeat',
                    help='Provide how many times to repeat the message. Defaults to 1',
                    type=int
                    )
parser.add_argument('-I', '--interval',
                    default=15,
                    dest='interval',
                    help='Provide how many seconds to wait before repeating the message. Defaults to 15 seconds',
                    type=int
                    )
parser.add_argument('-V', '--voice',
                    default=1,
                    dest='voice',
                    help='Provide how many times to repeat the message. Defaults to 1',
                    type=int
                    )
parser.add_argument('-D', '--debug',
                    default=False,
                    action=argparse.BooleanOptionalAction,
                    dest='debug',
                    help='Prints the server response'
                    )
parser.add_argument('-J', '--outputjson',
                    default=False,
                    action=argparse.BooleanOptionalAction,
                    dest='outputjson',
                    help='For list command only. Output voices in JSON format'
                    )                    
args = parser.parse_args()
args.command = args.command.lower()
if args.command == 'list':
    message = {
        "command": 'list',
    }
else:
    message = {
        "command": args.command,
        "message": args.message,
        "repeat": args.repeat,
        "interval": args.interval,
        "voice": args.voice
    }
run(tcp_echo_client(args.command, args.host, args.port, json.dumps(
    message), args.debug, args.outputjson), stop_on_unhandled_errors=True)
