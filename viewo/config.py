# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila
import writers

import viewo

SECRET_KEY = configo.env('CHANIA_SECRET_KEY', os.urandom(64))

TEMPLATES = os.path.join(viewo.ROOT, 'viewo/templates')
STATIC = os.path.join(viewo.ROOT, 'viewo/static')

# 20 megabyte
FILE_SIZE_MAX = configo.env('CHANIA_DOCUMENT_SIZE_MAX', 20 * 1024 * 1024)

API_PREFIX = '/api/v0'

VISITORS_FILE_SIZE_MAX = 1024  # kb
VISITORS_TRACKING = configo.env('CHANIA_VISITORS_TRACKING', True)
VISITORS_TRACKING_STATIC = configo.env('CHANIA_VISITORS_TRACKING_STATIC', False)

PASSWORD_LENGTH_MIN = 8
PASSWORD_LENGTH_MAX = 64

# null:disable caching
CACHING = configo.env('CHANIA_CACHING', 'null')

OPTIMIZE_DATA = configo.env('CHANIA_OPTIMIZE_DATA', False)

PAYMENT = configo.env('CHANIA_PAYMENT', False)

TALKER = configo.env('CHANIA_TALKER', True)


def config_show():
    utila.debug('')
    utila.debug('USER')
    utila.debug('')
    utila.debug(f'PAYMENT:             {PAYMENT}')
    utila.debug(f'TALKER:              {TALKER}')
    utila.debug(f'VISITORS_TRACKING:   {VISITORS_TRACKING}')
    utila.debug(f'PASSWORD_LENGTH_MIN: {PASSWORD_LENGTH_MIN}')
    utila.debug('')
    utila.debug('PLATFORM')
    utila.debug('')
    utila.debug(f'API_PREFIX:          {API_PREFIX}')
    utila.debug(f'FILE_SIZE_MAX:       {FILE_SIZE_MAX}')
    utila.debug('')


def writing() -> str:
    """Return path to generated `writers club` content.

    If content is not generated, run writer generator.
    """
    result = writers.build()
    if not os.path.exists(result):
        completed = writers.generate()
        assert completed == utila.SUCCESS
    assert os.path.exists(result), str(result)
    return result
