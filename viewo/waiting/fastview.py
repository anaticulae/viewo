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
import re

import protocol
import utila

import viewo.waiting
import viewo.waiting.data


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
    path = viewo.waiting.data.fastview_result(process)
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
        parsed = load_fastview_group_result(os.path.join(path, group))
        if not parsed:
            utila.error(f'could not parse {parsed}')
            continue
        result.append(parsed)
    return result


PATTERN = re.compile(r'\w+__(?P<filename>\w+)_user\.yaml')


def load_fastview_group_result(path: str) -> viewo.waiting.FastViewGroupStatus:
    assert os.path.exists(path), str(path)
    _, title = os.path.split(path)
    title = title[3:]  # remove leading digit/digit/underline
    files = [
        item for item in os.listdir(path)
        if os.path.isfile(os.path.join(path, item)) and item.endswith('.yaml')
    ]
    error = []
    for name in files:
        if not PATTERN.match(name):
            utila.error(f'{name} does not match file pattern - skip')
            continue
        loaded = protocol.load_result(os.path.join(path, name))
        for finding in loaded:
            error.append(finding.solution.title)
    return viewo.waiting.FastViewGroupStatus(title=title, error=error)
