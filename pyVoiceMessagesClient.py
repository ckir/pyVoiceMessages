import asyncio
from aiorun import run
import json
import argparse
import datetime
from rich.console import Console
from rich.table import Table


async def tcp_echo_client(command, host, port, message, debug, outputjson):
    try:
        reader, writer = await asyncio.open_connection(host, port)

        writer.write(message.encode())

        data = await reader.read(8192)
        data = data.decode()
        if debug:
            print(datetime.datetime.now().isoformat(), "Server said: %r" % data)

        writer.close()
        data = json.loads(data)
        if command == "list":
            if outputjson:
                print(json.dumps(data["response"], indent=4))
            else:
                table = Table(title="Available Voices")
                table.add_column("#")
                for header in next(iter(data["response"].values())).keys():
                    table.add_column(header.title())
                for voice in data["response"]:
                    vdata = data["response"][voice]
                    if "languages" in vdata and isinstance(vdata["languages"], list):
                        vdata["languages"] = ":".join(vdata["languages"])
                    row = list(vdata.values())
                    row.insert(0, voice)
                    table.add_row(*row)
                console = Console()
                console.print(table)

    except Exception as e:
        print(datetime.datetime.now().isoformat(), repr(e))

    asyncio.get_event_loop().stop()

def start_list(args):
    message = {
        "command": "list",
    }
    run(
        tcp_echo_client(
            'list',
            args.host,
            args.port,
            json.dumps(message),
            args.debug,
            args.outputjson,
        ),
        stop_on_unhandled_errors=True,
    )    

def start_on(args):
    message = {
        "command": "on",
        "message": args.message,
        "repeat": args.repeat,
        "interval": args.interval,
        "voice": args.voice,
    }
    run(
        tcp_echo_client(
            "on",
            args.host,
            args.port,
            json.dumps(message),
            args.debug,
            None,
        ),
        stop_on_unhandled_errors=True,
    )

def start_off(args):
    message = {
        "command": "off",
        "message": args.message,
        "repeat": None,
        "interval": None,
        "voice": None,
    }
    run(
        tcp_echo_client(
            "off",
            args.host,
            args.port,
            json.dumps(message),
            args.debug,
            None,
        ),
        stop_on_unhandled_errors=True,
    )    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        default="localhost",
        dest="host",
        help="Provide destination host. Defaults to localhost",
        type=str,
    )
    parser.add_argument(
        "-P",
        "--port",
        default=8888,
        dest="port",
        help="Provide destination port. Defaults to 8888",
        type=int,
    )
    parser.add_argument(
        "-D",
        "--debug",
        default=False,
        action=argparse.BooleanOptionalAction,
        dest="debug",
        help="Prints the server response",
    )

    sub_parsers = parser.add_subparsers(title='Subcommands',
                                   description='valid subcommands',
                                   help='additional help')

    parser_list = sub_parsers.add_parser("list", help="List server voices")
    parser_list.add_argument(
        "-J",
        "--outputjson",
        default=False,
        action=argparse.BooleanOptionalAction,
        dest="outputjson",
        help="Output voices in JSON format",
    )
    parser_list.set_defaults(func=start_list)

    parser_on = sub_parsers.add_parser("on", help="Create new message")
    parser_on.add_argument("message", help="Provide text to say", type=str)
    parser_on.add_argument(
        "-R",
        "--repeat",
        default=1,
        dest="repeat",
        help="Provide how many times to repeat the message. Defaults to 1",
        type=int,
    )
    parser_on.add_argument(
        "-I",
        "--interval",
        default=15,
        dest="interval",
        help="Provide how many seconds to wait before repeating the message. Defaults to 15 seconds",
        type=int,
    )
    parser_on.add_argument(
        "-V",
        "--voice",
        default=1,
        dest="voice",
        help="Provide how many times to repeat the message. Defaults to 1",
        type=int,
    )
    parser_on.set_defaults(func=start_on)

    parser_off = sub_parsers.add_parser("off", help="Cancel existing message")
    parser_off.add_argument("message", help="Message to cancel", type=str)
    parser_off.set_defaults(func=start_off)
    
    args = parser.parse_args()
    args.func(args)
