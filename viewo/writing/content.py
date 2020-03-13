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

CSS = f'<link href="/_static/wclub.css" rel="stylesheet" type="text/css">'
JS = """<script type="text/javascript" src="/_static/jquery.js"></script>
<script type="text/javascript" id="documentation_options" data-url_root="./" src="_static/documentation_options.js"></script>
    <script type="text/javascript" src="_static/jquery.js"></script>
    <script type="text/javascript" src="_static/underscore.js"></script>
    <script type="text/javascript" src="_static/doctools.js"></script>
    <script type="text/javascript" src="_static/language_data.js"></script>
    <script type="text/javascript" src="_static/translations.js"></script>"""


def replace(content: str, source: str) -> str:
    # strip body
    content = viewo.config.content(content)

    if source == os.path.join(viewo.config.writing(), 'index.html'):
        # HACK: fix main links
        content = content.replace('action="search.html"', 'action="writing/search.html"') # yapf:disable
        content = content.replace('href="#', 'href="index.html#')
        content = content.replace('href="', 'href="writing/')

    # add css and javascript
    content = f'{CSS}\n{JS}\n{content}'
    return content
