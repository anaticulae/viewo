# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import json
import os

import link
import protocol
import utila

import viewo.waiting


def load_resultview_result(process: str) -> str:
    result = link.resultview(process)
    if not os.path.exists(result):
        return None
    return load_resultview(result)


def load_resultview(path: str) -> viewo.waiting.ResultPageViews:
    assert os.path.exists(path), str(path)
    files = [item for item in os.listdir(path) if item.endswith('.yaml')]

    findings = []
    for item in files:
        loaded = protocol.load_result(os.path.join(path, item))
        findings.extend(loaded)
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
            html=content,
            findings=finding,
        )
        result.append(item)
    return result


def pages(html, grouped) -> list:
    collected = []
    # TODO: IMPROVE THIS TO SUPPORT SELECTIVE PAGES
    collected.extend(list(range(len(html))))
    collected.extend([item.page for item in grouped])
    result = set(collected)
    result = sorted(result)
    return result


def tojson(items: viewo.waiting.ResultPageViews) -> str:
    result = []
    for item in items:
        findings = [{
            'number': finding.number,
            'location': {
                'page': finding.location.page,
            },
            'title': finding.solution.title,
            'message': finding.solution.description,
            'status': finding.solution.status.value,
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


def load_htmlview(path: str) -> list:
    assert os.path.exists(path), str(path)
    # Sort html pages by number, sort 0, 1, 2, 3, ..., 10, 11, 12 correctly.
    # Example: 0.html, cut file extention and make file name int-sortable.
    files = sorted(os.listdir(path), key=lambda x: int(str(x).split('.')[0]))
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
