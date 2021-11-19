# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os

import iamraw
import iamraw.path
import link
import serializeraw
import utila


def load_sentences(path: str) -> dict:
    # TODO: REFACTOR WITH FEEDBACK
    words = serializeraw.load_text(path)
    pagesentences = collections.defaultdict(list)
    for page in words:
        for _, sentences in page.content:
            for sentence in sentences:
                pagesentences[page.page].append(sentence)
    # enable KeyError
    pagesentences = dict(pagesentences)  # pylint:disable=R0204
    return pagesentences


def load_sentences_fromdocumentid(documentid: str) -> str:
    result = link.resultview(documentid, done=True)
    if not os.path.exists(result):
        return None
    path = os.path.join(result, 'words__word_result.yaml')
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    return load_sentences(path)


def load_footenotes(path: str):
    footerheaders = serializeraw.load_headerfooter(path)
    result = []
    for page in footerheaders:
        footer = page.footer
        if not footer:
            continue
        try:
            notes = footer.notes
        except AttributeError:
            continue
        result.append((page.page, notes))
    return result


def load_pagenumbers_fromdocumentid(documentid: str) -> dict:
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
    >>> fill_pages({'0': "I", '1': "II", '3': "IV", '4': "V", '5': "1", '6': "2", '8': "4"}, pdflength=10)
    {'0': 'I', '1': 'II', '2': '[3]', '3': 'IV', '4': 'V', '5': '1', '6': '2', '7': '[8]', '8': '4', '9': '[10]'}
    """
    for page in range(pdflength):
        key = str(page)
        if key in pages:
            continue
        pages[key] = f'[{page+1}]'
    # sort dict by page number
    pages = {key: pages[key] for key in sorted(pages.keys(), key=int)}
    return pages


def load_footnotes_fromdocumentid(documentid: str):
    result = link.resultview(documentid, done=True)
    if not os.path.exists(result):
        return None
    path = iamraw.path.headerfooters(result)
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    return load_footenotes(path)


def load_doctextstyle_fromdocumentid(documentid: str):
    result = link.resultview(documentid, done=True)
    if not os.path.exists(result):
        return None
    path = os.path.join(result, 'doctextstyle__textstyle.yaml')
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    loaded = serializeraw.load_doctextstyle(path)

    fontstore = serializeraw.create_fontstore_frompath(result, prefix='oneline')
    if fontstore:
        # replace font ids with user readable font text
        for key in [
                'footnote_family',
                'h1_family',
                'h2_family',
                'h3_family',
                'pagenumber_family',
                'text_family',
        ]:
            if not getattr(loaded, key):
                continue
            font = getattr(loaded, key)
            font = fontstore[font]
            if font is None:
                utila.error(f'could not find font id: {font}')
                continue
            font = friendly_font(font.name)
            setattr(loaded, key, font)
    return loaded


def friendly_font(font: str) -> str:
    """\
    >>> friendly_font('TimesNewRoman')
    'Times New Roman'
    """
    font = font.lower()
    if font == 'timesnewroman':
        return 'Times New Roman'
    return font


def load_captions_fromdocumentid(documentid: str) -> iamraw.PageContentCaptions:
    result = link.resultview(documentid, done=True)
    if not os.path.exists(result):
        return None
    path = utila.pathconnector(result, 'caption', 'general_general')
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    return serializeraw.load_captions(path)


def load_links_fromdocumentid(documentid: str) -> iamraw.PageContentCaptions:
    result = link.resultview(documentid, done=True)
    if not os.path.exists(result):
        return None
    path = utila.pathconnector(result, 'words', 'links_links')
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    return serializeraw.load_hyperlinks(path)


def load_bibliography_fromdocumentid(documentid: str) -> iamraw.BibliographyReferences:  # yapf:disable
    result = link.resultview(documentid, done=True)
    if not os.path.exists(result):
        return None
    path = utila.pathconnector(result, 'detector', 'bibliography_detected')
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    return serializeraw.load_bibliography_reference(path)
