# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import collections
import sys

import utila


def main():
    config = eval_cli()
    # setup logging
    utila.level_setup(level=config.verbose)
    app = create_app()
    # run app
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug,
    )


Config = collections.namedtuple(
    'Config',
    'host, port, debug, verbose',
)


def eval_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost', help='run on url')
    parser.add_argument('--port', default=5000, help='run on port')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='run in debug mode',
    )
    parser.add_argument(
        '--verbose',
        '-V',
        action='count',
        default=0,
        help='define level of logging',
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='print version and quit',
    )
    argv = parser.parse_args()
    if argv.version:
        import viewo
        utila.log(viewo.__version__)
        sys.exit(utila.SUCCESS)
    result = Config(
        argv.host,
        int(argv.port),
        argv.debug,
        argv.verbose,
    )
    return result


def create_app():
    import viewo.app
    result = viewo.app.create_app()
    return result
