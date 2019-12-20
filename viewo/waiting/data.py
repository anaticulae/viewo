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
import utila

from viewo.waiting import FASTVIEW
from viewo.waiting import VERIFY
from viewo.waiting import FastViewGroupStatus
from viewo.waiting import FastViewStatus
from viewo.waiting import State
from viewo.waiting import Status


def jsonify(item: Status) -> str:
    """Dump `Status` to json.

    Args:
        item(Status): status of current waiting room
    Returns:
        `Status` as json representation
    """
    states = []
    raw = {
        'status': item.status.value,
        'states': states,
    }
    for state in item.state:
        states.append(state.value)
    result = json.dumps(raw)
    return result


def fastviewstatus_tojson(current: FastViewStatus) -> str:
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


def loads(content: str) -> Status:
    loaded = json.loads(content)
    result = Status()
    result.status = State.fromstr(loaded['status'])
    for item in loaded['states']:
        parsed = State.fromstr(item)
        result.append(parsed)  # pylint:disable=E1101
    return result


def status(process: str) -> Status:  # pylint:disable=too-complex
    # TODO: REPLACE WITH BETTER PYTHON STATE MACHINE LIBRARY
    todo = configo.todo()
    working = os.path.join(todo, process)
    if not os.path.exists(working):
        # TODO: CHECK ACCESS RIGHTS
        # process does not exists
        return None

    pdf = os.path.join(working, process)

    def uploaded():
        return State.done if os.path.exists(pdf) else State.running

    def verified():
        verifypath = os.path.join(working, VERIFY)
        verify = State.running if uploaded() == State.done else State.waiting
        if os.path.exists(verifypath):
            content = utila.file_read(verifypath).strip()
            if content == '{}':
                verify = State.failed
            else:
                verify = State.done
        return verify

    def analyzestarted():
        before = verified()
        if before == State.failed:
            return State.failed
        if before == State.waiting:
            return State.waiting
        if fastview_result(process):
            return State.done
        if before == State.done:
            return State.running
        return State.waiting

    def fastviewed():
        before = analyzestarted()
        if before == State.failed:
            return State.failed
        path = fastview_result(process)
        if path is None:
            return State.waiting
        if os.path.exists(os.path.join(path, 'done')):
            return State.done
        if os.path.exists(os.path.join(path, 'failed')):
            return State.failed
        if before == State.done:
            return State.running
        return State.waiting

    def globalviewed():
        before = analyzestarted()
        before_fast = fastviewed()
        if before == State.failed or before_fast == State.failed:
            return State.failed
        path = result_result(process)
        if path is None:
            return State.waiting
        if os.path.exists(os.path.join(path, 'done')):
            return State.done
        if os.path.exists(os.path.join(path, 'failed')):
            return State.failed
        if before == State.done:
            return State.running
        return State.waiting

    def presented():
        before = globalviewed()
        if before == State.failed:
            return State.failed
        if before == State.done:
            if copy_done(process):
                return State.done
            return State.running
        return State.waiting

    result = Status(
        State.running,
        [
            uploaded(),
            verified(),
            analyzestarted(),
            fastviewed(),
            globalviewed(),
            presented()
        ],
    )

    if all([item == State.done for item in result]):
        result.status = State.done
    if any([item == State.running for item in result]):
        result.status = State.running  # pylint:disable=redefined-variable-type
    if any([item == State.failed for item in result]):
        result.status = State.failed
    return result


def load_validation_result(process: str) -> dict:
    """Load validation result from `todo` or `ready` path depending on
    processing status.

    Args:
        process(string): identifier interesseted validation process
    Returns:
        - dict with pages, editor and pdf version or
        - empty dict if validation fails or
        - None if process does not exists
    """
    process = str(process)
    ready = configo.ready()
    ready = os.path.join(ready, process)
    todo = configo.todo()
    todo = os.path.join(todo, process)
    path = None
    if os.path.exists(todo):
        path = todo
    if os.path.exists(ready):
        path = ready

    if path is None:
        # invalid process
        return None
    data = os.path.join(path, VERIFY)
    data = utila.file_read(data)
    loaded = json.loads(data)
    return loaded


def load_fastview_result(process: str) -> FastViewStatus:
    path = fastview_result(process)
    if path is None:
        return None
    groups = [
        item for item in os.listdir(path)
        if os.path.isdir(os.path.join(path, item))
    ]
    groups = sorted(groups)
    result = FastViewStatus()
    for group in groups:
        if not group[0:2].isnumeric():
            # check that content folder start with number which is 2
            # digits longs.
            # Pattern [0-9]{2}\_\w+
            continue
        title = group[3:]
        item = FastViewGroupStatus(title=title)
        result.append(item)
    return result


def fastview_result(process: str) -> str:
    todo = configo.todo()
    todo = os.path.join(todo, process)
    fastview = os.path.join(todo, FASTVIEW)
    if os.path.exists(fastview):
        return fastview
    return None


def result_result(process: str) -> str:
    todo = configo.todo()
    todo = os.path.join(todo, process)
    fastview = os.path.join(todo, 'result')
    if os.path.exists(fastview):
        return fastview
    return None


def copy_done(process: str) -> bool:
    ready = configo.ready()
    ready = os.path.join(ready, process)
    if os.path.exists(ready):
        return True
    return False
