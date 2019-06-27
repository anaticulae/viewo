# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from flask import current_app
from utila import file_read

from viewo import create_application
from viewo.config import ROOT
from viewo.config import TEMPLATES

TEST_DATA = join(ROOT, 'tests/data')
assert exists(TEST_DATA), TEST_DATA

BASE_TEMPLATE = file_read(join(TEMPLATES, 'base.html'))

MINIMAL = join(TEST_DATA, 'minimal.pdf')
assert exists(MINIMAL), MINIMAL

EXAMPLE_READY = join(TEST_DATA, 'ready')
assert exists(EXAMPLE_READY), EXAMPLE_READY

EXAMPLE_RESULT = join(EXAMPLE_READY, '1508790764/result')
assert exists(EXAMPLE_RESULT), EXAMPLE_RESULT


def decode(response) -> str:
    """Read binary data from response and convert them to str"""
    return response.data.decode('utf8')
