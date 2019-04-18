# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os
from os.path import exists
from os.path import join

from utila import FAILURE
from utila import logging_error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 Megabyte

SECRET_KEY = b'helmut_max_power_abs29.nsTODOThisIsVerySecreyISwarTODO'

TEMPLATES = join(ROOT, 'viewo/templates')
STATIC = join(ROOT, 'viewo/static')


def environment():
    """Return `SHARED_TODO` and `SHARED_READY` folder"""
    try:
        todo = os.environ['SHARED_TODO']
        ready = os.environ['SHARED_READY']
    except KeyError as error:
        logging_error('MISSING ENVIRONMENT VARS %s' % error)
        exit(FAILURE)
    else:
        # Check existence of both folder
        ret = 0
        if not exists(todo):
            logging_error('Location does not exists: %s' % todo)
            ret += 1
        if not exists(ready):
            logging_error('Location does not exists: %s' % ready)
            ret += 1
        if ret:
            exit(FAILURE)
    return todo, ready
