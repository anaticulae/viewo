# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila


def docs_url() -> str:
    # TODO: MOVE TO CONFIGO
    try:
        url = os.environ['HELPY_DOCS']
    except KeyError:
        url = 'http://127.0.0.1:5555'
        utila.error(f'no env var `HELPY_DOCS` - use default url {url}')
    if not url.endswith('/'):
        url = f'{url}/'
    return url
