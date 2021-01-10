# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import writers
import writers.generator

import viewo

MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 Megabyte

SECRET_KEY = b'helmut_max_power_abs29.nsTODOThisIsVerySecreyISwarTODO'

TEMPLATES = os.path.join(viewo.ROOT, 'viewo/templates')
STATIC = os.path.join(viewo.ROOT, 'viewo/static')

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

API_PREFIX = '/api/v0'

VISITORS_MAX_FILE_SIZE = 1024  # kb
VISITORS_TRACKING = True
VISITORS_TRACK_STATIC_REQUESTS = False

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64


def writing() -> str:
    """Return path to generated `writers club` content. If content is
    not generated, writer generator is executed."""
    result = writers.build()
    if not os.path.exists(result):
        completed = writers.generator.generate()
        assert completed == utila.SUCCESS
    assert os.path.exists(result), str(result)
    return result
