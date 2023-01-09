# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import viewo.api.writing


def replace(content: str, source: str) -> str:
    # strip body
    content = body(content)
    docpage = os.path.join(viewo.api.writing.DOC_PATH, 'index.html')
    if source == docpage:
        # TODO: REPLACE WITH SPHINX WEBDRIVER
        # HACK: fix main links
        content = content.replace('action="search.html"', 'action="writing/search.html"') # yapf:disable
        content = content.replace('href="#', 'href="index.html#')
        content = content.replace('href="', 'href="writing/')
    content += '<style>h1{padding-bottom:0px;</style>'
    return content


def body(raw: str) -> str:
    pattern = r'<body>(?P<content>.*)</body>'
    matched = re.search(pattern, raw, re.DOTALL)
    if not matched:
        return raw
    return matched['content']
