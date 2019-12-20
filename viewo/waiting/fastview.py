# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import json
import os

import configo

import viewo.waiting


def fastviewstatus_tojson(current: viewo.waiting.FastViewStatus) -> str:
    if not current:
        return '{}'
    items = []
    for item in current:
        error = [str(item) for item in item.error]
        good = [str(item) for item in item.good]
        warning = [str(item) for item in item.warning]
        raw = {
            'title': item.title,
            'pages': item.pages,
            'content': {
                'error': error,
                'good': good,
                'warning': warning,
            }
        }
        items.append(raw)
    result = {
        'status': current.status.value,
        'content': items,
    }
    dumped = json.dumps(result)
    return dumped


def load_fastview_result(process: str) -> viewo.waiting.FastViewStatus:
    path = fastview_result(process)
    if path is None:
        return None
    groups = [
        item for item in os.listdir(path)
        if os.path.isdir(os.path.join(path, item))
    ]
    groups = sorted(groups)
    result = viewo.waiting.FastViewStatus()
    for group in groups:
        if not group[0:2].isnumeric():
            # check that content folder start with number which is 2
            # digits longs.
            # Pattern [0-9]{2}\_\w+
            continue
        title = group[3:]
        item = viewo.waiting.FastViewGroupStatus(title=title)
        result.append(item)
    return result


def fastview_result(process: str) -> str:
    todo = configo.todo()
    todo = os.path.join(todo, process)
    fastview = os.path.join(todo, viewo.waiting.FASTVIEW)
    if os.path.exists(fastview):
        return fastview
    return None
