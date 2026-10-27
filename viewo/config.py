# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import utilo
import writers

import viewo

SECRET_KEY = configos.env('CHANIA_SECRET_KEY', os.urandom(64))

TEMPLATES = os.path.join(viewo.ROOT, 'viewo/templates')
STATIC = os.path.join(viewo.ROOT, 'viewo/static')

# 20 megabyte
FILE_SIZE_MAX = configos.env('CHANIA_DOCUMENT_SIZE_MAX', 20 * 1024 * 1024)

API_PREFIX = '/api/v0'

VISITORS_FILE_SIZE_MAX = 1024  # kb
VISITORS_TRACKING = configos.env('CHANIA_VISITORS_TRACKING', True)
VISITORS_TRACKING_STATIC = configos.env('CHANIA_VISITORS_TRACKING_STATIC',
                                        False)

PASSWORD_LENGTH_MIN = 8
PASSWORD_LENGTH_MAX = 64

# null:disable caching
CACHING = configos.env('CHANIA_CACHING', 'NullCache')

OPTIMIZE_DATA = configos.env('CHANIA_OPTIMIZE_DATA', False)

PAYMENT = configos.env('CHANIA_PAYMENT', False)

TALKER = configos.env('CHANIA_TALKER', True)

PRODUCTION = configos.env('CHANIA_PRODUCTION', False)


def config_show():
    utilo.debug('')
    utilo.debug('USER')
    utilo.debug('')
    utilo.debug(f'PAYMENT:             {PAYMENT}')
    utilo.debug(f'TALKER:              {TALKER}')
    utilo.debug(f'VISITORS_TRACKING:   {VISITORS_TRACKING}')
    utilo.debug(f'PASSWORD_LENGTH_MIN: {PASSWORD_LENGTH_MIN}')
    utilo.debug('')
    utilo.debug('PLATFORM')
    utilo.debug('')
    utilo.debug(f'API_PREFIX:          {API_PREFIX}')
    utilo.debug(f'FILE_SIZE_MAX:       {FILE_SIZE_MAX}')
    utilo.debug('')


def writing() -> str:
    """Return path to generated `writers club` content.

    If content is not generated, run writer generator.
    """
    result = writers.build()
    if not os.path.exists(result):
        completed = writers.generate()
        assert completed == utilo.SUCCESS
    assert os.path.exists(result), str(result)
    return result
