# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from time import localtime
from time import time


def today() -> str:
    """Determine date in `german` format"""
    cur = localtime(time())
    return "%02d.%02d.%04d" % (cur.tm_mday, cur.tm_mon, cur.tm_year)


def current() -> str:
    """Determine time in `german` format"""
    cur = localtime(time())
    return "%02d:%02d" % (cur.tm_hour, cur.tm_min)


def time_and_date():
    return '%s %s' % (current(), today())
