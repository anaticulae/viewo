# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw.path
import link
import serializeraw
import utila


def load_fromdocumentid(documentid: str) -> dict:
    resultview = link.resultview(documentid, done=True)
    if not os.path.exists(resultview):
        return None
    path = iamraw.path.groupme_pagenumbers(resultview)
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    pagenumbers = serializeraw.load_pagenumbers(path)
    result = {page.pdfpage: page.detected for page in pagenumbers}
    pdfinfo = link.pdfinfo(documentid)
    if pdfinfo:
        result = fill_pages(result, pdflength=pdfinfo.pages)
    return result


def fill_pages(pages: dict, pdflength: int) -> dict:
    """\
    >>> fill_pages({0: "I", 1: "II", '3': "IV", 4: "V", '5': "1", '6': "2", '8': "4"}, pdflength=10)
    {0: 'I', 1: 'II', 2: '[3]', 3: 'IV', 4: 'V', 5: '1', 6: '2', 7: '[8]', 8: '4', 9: '[10]'}
    """
    pages = {int(key): value for key, value in pages.items()}
    for page in range(pdflength):
        if page in pages:
            continue
        # expected page
        pages[page] = f'[{page+1}]'
    # sort dict by page number
    pages = {key: pages[key] for key in sorted(pages.keys())}
    return pages
