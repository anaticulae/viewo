#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

PACKAGES = [
    'viewo',
    'viewo.api',
    'viewo.api.documents',
    'viewo.api.findings',
    'viewo.api.pageviews',
    'viewo.api.users',
    'viewo.api.visitors',
    'viewo.api_.findings',
    'viewo.result',
    'viewo.result.loader',
    'viewo.user',
    'viewo.view',
    'viewo.waiting',
    'viewo.writing',
]
ENTRY_POINTS = {
    'console_scripts': ['viewo = viewo.cli:main',],
}

if __name__ == "__main__":
    utila.install(__file__)
