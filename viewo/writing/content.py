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

CSS = f'<link href="/build/_static/wclub.css" rel="stylesheet" type="text/css">'
JS = """<script type="text/javascript" src="/build/_static/jquery.js"></script>
<script type="text/javascript" id="documentation_options"
data-url_root="/build/" src="/build/_static/documentation_options.js"></script>
<script type="text/javascript" src="/build/_static/jquery.js"></script>
<script type="text/javascript" src="/build/_static/underscore.js"></script>
<script type="text/javascript" src="/build/_static/doctools.js"></script>
<script type="text/javascript" src="/build/_static/language_data.js"></script>
<script type="text/javascript" src="/build/_static/translations.js"></script>"""

JS_SEARCH = """
<script type="text/javascript" src="/build/_static/searchtools.js"></script>
<script type="text/javascript">
jQuery(function() { Search.loadIndex("/build/searchindex.js"); });
</script>
<script type="text/javascript" id="searchindexloader"></script>
"""


def replace(content: str, source: str) -> str:
    # strip body
    content = viewo.config.content(content)

    docpage = os.path.join(viewo.config.writing(), 'index.html')
    if source == docpage:
        # HACK: fix main links
        content = content.replace('action="search.html"', 'action="writing/search.html"') # yapf:disable
        content = content.replace('href="#', 'href="index.html#')
        content = content.replace('href="', 'href="writing/')

    content = f'{JS_SEARCH}\n{content}'

    # add css and javascript
    content = f'{CSS}\n{JS}\n{content}'
    return content
