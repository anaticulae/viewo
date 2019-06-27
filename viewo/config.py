# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 Megabyte

SECRET_KEY = b'helmut_max_power_abs29.nsTODOThisIsVerySecreyISwarTODO'

TEMPLATES = os.path.join(ROOT, 'viewo/templates')
STATIC = os.path.join(ROOT, 'viewo/static')
