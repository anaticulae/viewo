# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utila


def replace(content: str):
    replaced = replace_links(content, REFLINKS)
    return replaced


def replace_links(content: str, table: dict) -> str:
    """Replace reflinks in generated html code.

    >>> replace_links('rnal" href="{amazon:theissen_2017}">Theissen:2017;',
    ... table={'amazon:theissen_2017': 'http://amazon.com/helm/theissen'})
    'rnal" href="http://amazon.com/helm/theissen">Theissen:2017;'
    """
    pattern = r'{(?P<store>\w+):(?P<product>\w+)}'
    matched = re.findall(pattern, content)
    if not matched:
        return content
    for item in matched:
        finding = '%s:%s' % item
        token = '{%s}' % finding
        try:
            replacement = table[finding]
        except KeyError:
            utila.error(f'could find ref link for {finding}')
            continue
        content = content.replace(token, replacement, 1)
    return content


REFLINKS = {
    'amazon:theissen_2017': 'http://amazon.com/helm/theissen',
}
