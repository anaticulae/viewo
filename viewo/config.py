# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila
import writers
import writers.generator

import viewo

SECRET_KEY = configo.env('CHANIA_SECRET_KEY', os.urandom(64))

TEMPLATES = os.path.join(viewo.ROOT, 'viewo/templates')
STATIC = os.path.join(viewo.ROOT, 'viewo/static')

# 20 megabyte
MAX_FILE_SIZE = configo.env('CHANIA_DOCUMENT_SIZE_MAX', 20 * 1024 * 1024)

API_PREFIX = '/api/v0'

VISITORS_MAX_FILE_SIZE = 1024  # kb
VISITORS_TRACKING = configo.env('CHANIA_VISITORS_TRACKING', True)
VISITORS_TRACKING_STATIC = configo.env('CHANIA_VISITORS_TRACKING_STATIC', False)

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64

# null:disable caching
CACHING = configo.env('CHANIA_CACHING', 'null')

OPTIMIZE_DATA = configo.env('CHANIA_OPTIMIZE_DATA', False)


def writing() -> str:
    """Return path to generated `writers club` content. If content is
    not generated, writer generator is executed."""
    result = writers.build()
    if not os.path.exists(result):
        completed = writers.generator.generate()
        assert completed == utila.SUCCESS
    assert os.path.exists(result), str(result)
    return result
