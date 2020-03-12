# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os
import re

import utila
import writers
import writers.generator

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 Megabyte

SECRET_KEY = b'helmut_max_power_abs29.nsTODOThisIsVerySecreyISwarTODO'

TEMPLATES = os.path.join(ROOT, 'viewo/templates')
STATIC = os.path.join(ROOT, 'viewo/static')


def writing() -> str:
    """Return path to generated `writers club` content. If content is
    not generated, writer generator is executed."""
    result = writers.build()
    if not os.path.exists(result):
        completed = writers.generator.generate()
        assert completed == utila.SUCCESS
    assert os.path.exists(result), str(result)
    return result


def content(raw: str) -> str:
    pattern = r'<body>(?P<content>.*)</body>'
    matched = re.search(pattern, raw, re.DOTALL)
    if not matched:
        return raw
    return matched['content']
