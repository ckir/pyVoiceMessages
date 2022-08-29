import asyncio
from aiorun import run
import json
import argparse


async def tcp_echo_client(host, port, message, verbose):
    reader, writer = await asyncio.open_connection(
        host, port)

    writer.write(message.encode())

    data = await reader.read(8192)
    if verbose:
        print('Server said: %r' % data.decode())

    writer.close()
    asyncio.get_event_loop().stop()


parser = argparse.ArgumentParser()
parser.add_argument('switch',
                    choices=('on', 'off'),
                    help='Provide operation. On = create new message / off = cancel existing message',
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
                    help='Provide how many times to repeat the message. Defults to 1',
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
parser.add_argument('-Q', '--quiet',
                    default=True,
                    action=argparse.BooleanOptionalAction,
                    dest='verbose',
                    help='Prints the server response'
                    )
args = parser.parse_args()
message = {
    "switch": args.switch,
    "message": args.message,
    "repeat": args.repeat,
    "interval": args.interval,
    "voice": args.voice
}
run(tcp_echo_client(args.host, args.port, json.dumps(message), args.verbose), stop_on_unhandled_errors=True)
