#!/usr/bin/env python3

import argparse
import logging
import sys
import asyncio

from .wavemeter import Wavemeter

from sipyco.pc_rpc import Server
from sipyco import common_args


logger = logging.getLogger(__name__)


def get_argparser():
    parser = argparse.ArgumentParser(
        description="""HighFinesse Wavemeter controller""")
    parser.add_argument(
        "-d", "--device", default=None,
        help="Device host name or IP address")
    parser.add_argument(
        "-o", "--device-port", default=1234,
        help="Device TCP port number")
    common_args.simple_network_args(parser, 3273)
    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)

    if args.device is None:
        print("You need to supply a -d/--device "
              "argument. Use --help for more information.")
        sys.exit(1)

    loop = asyncio.get_event_loop()

    async def run():
        with await Wavemeter.connect(
                args.device, port=args.device_port, loop=loop) as dev:
            # only wavemeter
            # logger.debug("connected, version %s", await dev.get_version())
            server = Server({"wavemeter": dev}, None, True)
            await server.start(common_args.bind_address_from_args(args), args.port)
            try:
                await server.wait_terminate()
            finally:
                await server.stop()

    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    main()
