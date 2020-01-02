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

import configo
import protocol
import utila

import viewo.waiting


def load_resultview_result(process: str) -> str:
    todo = configo.todo()
    result = os.path.join(todo, process, 'result')
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
    grouped = protocol.bylocation(findings)

    result = []
    htmlpath = os.path.join(path, '../view')
    html = HtmlLookup(htmlpath)
    for group in grouped:
        content = html[group.page]
        item = viewo.waiting.ResultPageView(
            page=group.page,
            html=content if content else '',
            findings=group.content,
        )
        result.append(item)
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
    content = [
        utila.file_read(os.path.join(path, item))
        for item in sorted(os.listdir(path))
    ]
    return content


class HtmlLookup:

    def __init__(self, path):
        self.data = []
        if os.path.exists(path):
            self.data = load_htmlview(path)

    def __getitem__(self, index):
        try:
            return self.data[index]
        except IndexError:
            return None
