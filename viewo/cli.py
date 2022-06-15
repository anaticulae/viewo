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

import utila

import viewo.app


def main():
    config = eval_cli()
    # setup logging
    utila.level_setup(level=config.verbose)
    # run app
    main_ = viewo.app.create_app()
    main_.run(
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
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=5000)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--verbose', '-V', action='count', default=0)
    argv = parser.parse_args()
    result = Config(
        argv.host,
        int(argv.port),
        argv.debug,
        argv.verbose,
    )
    return result
