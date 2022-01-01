# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re


def optimize(raw: str) -> str:
    # TODO: USE WEBSERVER INSTEAD
    response_type = raw.headers.get('Content-Type')
    html = 'text/html;' in response_type
    if not html:
        return raw
    # optimize
    response = raw.response
    assert len(response) == 1
    optimized = optimize_html(response[0].decode('utf8'))
    # update reponse
    raw.set_data(optimized)
    return raw


WHITESPACE = re.compile(r'(>)\s*(<)')


def optimize_html(raw: str) -> str:
    r"""\
    >>> optimize_html('    <HTML>   \n    </HTML>    \n\n ')
    '<HTML></HTML>'
    """
    raw = raw.strip()
    raw = WHITESPACE.sub('><', raw)
    raw = re.sub(r'<br />\s*', '<br/>', raw)
    raw = re.sub(r'\s*</p>*', '</p>', raw)
    raw = re.sub(r'\n\s*', '\n', raw)
    raw = re.sub(r'}\s*<', '}<', raw)
    raw = re.sub(r'{\s*', '{', raw)
    raw = re.sub(r';\s*', ';', raw)
    raw = re.sub(r'>\s*', '>', raw)
    # do not remove single space before
    raw = re.sub(r'\s{2,}<', '<', raw)
    raw = re.sub(r'"\s', '" ', raw)
    raw = re.sub(r'}\s*', '}', raw)
    raw = re.sub(r';<\s*', ';<', raw)
    return raw
