# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import viewo.config


def replace(content: str, source: str) -> str:
    # strip body
    content = viewo.config.content(content)

    docpage = os.path.join(viewo.config.writing(), 'index.html')
    if source == docpage:
        # TODO: REPLACE WITH SPHINX WEBDRIVER
        # HACK: fix main links
        content = content.replace('action="search.html"', 'action="writing/search.html"') # yapf:disable
        content = content.replace('href="#', 'href="index.html#')
        content = content.replace('href="', 'href="writing/')
    return content
