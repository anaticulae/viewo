# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import json
import os

import configo
import link
import protocol
import serializeraw
import utila
import writers

import viewo.utils
import viewo.waiting


def load_resultview_result(process: str) -> str:
    result = link.resultview(process)
    if not os.path.exists(result):
        return None
    return load_resultview(result, process)


def load_resultview(path: str, process: str) -> viewo.waiting.ResultPageViews:
    assert os.path.exists(path), str(path)
    files = [item for item in os.listdir(path) if item.endswith('.yaml')]

    findings = []
    for item in files:
        loaded = protocol.load_result(os.path.join(path, item))
        findings.extend(loaded)

    # TODO: unite with feedback enumerater
    for index, finding in enumerate(findings):
        finding.number = index

    grouped = {page.page: page for page in protocol.bylocation(findings)}

    result = []
    htmlpath = os.path.join(path, 'view')
    html = HtmlLookup(htmlpath)
    # load all pages not only the erroneous
    for page in pages(html, grouped.values()):
        # for page, rendered in enumerate(html):
        finding = grouped.get(page, None)
        finding = finding.content if finding else []
        try:
            content = html[page]
        except IndexError:
            content = ''
        # for group in grouped:
        # content = html[group.page]
        item = viewo.waiting.ResultPageView(
            page=page,
            html=patch_images(content, process),
            findings=finding,
        )
        result.append(item)
    return result


def patch_images(html: str, process: int) -> str:
    # TODO: REMOVE THIS HACK
    utila.error('patch images')
    html = html.replace('src="', f'src="{process}/')
    return html


def pages(html, grouped) -> list:
    collected = []
    # TODO: IMPROVE THIS TO SUPPORT SELECTIVE PAGES
    collected.extend(list(range(len(html))))
    collected.extend([item.page for item in grouped])
    result = set(collected)
    result = sorted(result)
    return result


def message_replace(content: str) -> str:
    url = configo.docs_url()
    content = writers.replace(content, url)
    # TODO: REMOVE VIEW HACK LATER
    content = content.replace('<a href', '<br/><br/><a href')
    return content


def selectable(location) -> int:
    """Page able only `location` is not selectable."""
    if location.value is None:
        return 0
    return 1


def tojson(
        items: viewo.waiting.ResultPageViews,
        pagesentences: dict = None,
) -> str:
    result = []
    for item in items:
        findings = [{
            'number': finding.number,
            'location': location_tojson(finding.location, pagesentences),
            'title': finding.solution.title,
            'message': message_replace(finding.solution.description),
            'status': finding.solution.status.value,
            'selectable': selectable(finding.location)
        } for finding in item.findings if finding.solution]
        result.append({
            'page': item.page,
            'html': item.html,
            'findings': findings,
        })
    raw = {
        'status': 0,
        'content': result,
    }
    dumped = json.dumps(raw)
    return dumped


def location_tojson(location, pagesentences: dict = None) -> dict:
    result = {
        'page': location.page,
    }
    # sentence, convert to words
    if location.shortcut == 's':
        result['sentence'] = location.value
        if pagesentences is not None:
            words = word_index(pagesentences, location.page, location.value)
            if words is None:
                utila.error(f'no words on page: {location.page}'
                            f' sentence: {location.value}')
            else:
                result['words'] = words
    return result


def word_index(pagesentences, page, sentence):
    result = []
    try:
        current = pagesentences[page]
    except KeyError:
        utila.log(f'could not access page: {page}')
        return result

    start = sum([len(items) for items in current[current:sentence]], start=0)

    for index, _ in enumerate(current[sentence], start=start):
        result.append(index)
    return result


def load_sentences(path: str) -> dict:
    # TODO: REFACTOR WITH FEEDBACK
    words = serializeraw.load_text(path)
    pagesentences = collections.defaultdict(list)
    for page, pagecontent in words:
        for _, sentences in pagecontent:
            for sentence in sentences:
                pagesentences[page].append(sentence)
    # enable KeyError
    pagesentences = dict(pagesentences)  # pylint:disable=R0204
    return pagesentences


def load_htmlview(path: str) -> list:
    # TODO: DANGEROUS
    assert os.path.exists(path), str(path)
    # Sort html pages by number, sort 0, 1, 2, 3, ..., 10, 11, 12 correctly.
    # Example: 0.html, cut file extention and make file name int-sortable.
    files = sorted(
        utila.file_list(path, 'html'), key=lambda x: int(str(x).split('.')[0]))
    content = [utila.file_read(os.path.join(path, item)) for item in files]
    return content


class HtmlLookup:

    def __init__(self, path):
        self.data = []
        if os.path.exists(path):
            self.data = load_htmlview(path)
        else:
            utila.error(f'html lookup: {path} does not exists.')

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)
