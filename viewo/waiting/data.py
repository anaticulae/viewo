# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import json
import os

import link
import utila

import viewo.path
from viewo.waiting import FASTVIEW
from viewo.waiting import VERIFY
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
        'progress': item.progress,
    }
    for state in item.state:
        states.append(state.value)
    result = json.dumps(raw)
    return result


def loads(content: str) -> Status:
    with contextlib.suppress(TypeError):
        content = json.loads(content)
    result = Status(status=State.fromstr(content['status']))
    for item in content['states']:
        parsed = State.fromstr(item)
        result.append(parsed)  # pylint:disable=E1101
    return result


def status(process: str) -> Status:  # pylint:disable=too-complex
    # TODO: REPLACE WITH BETTER PYTHON STATE MACHINE LIBRARY
    todo = viewo.path.todo()
    working = os.path.join(todo, process)
    if not os.path.exists(working):
        # TODO: CHECK ACCESS RIGHTS
        # process does not exists
        return None

    progress = link.progress(process)
    pdf = os.path.join(working, process)

    def uploaded():
        return State.DONE if os.path.exists(pdf) else State.RUNNING

    def verified():
        verifypath = os.path.join(working, VERIFY)
        verify = State.RUNNING if uploaded() == State.DONE else State.WAITING
        if os.path.exists(verifypath):
            content = utila.file_read(verifypath).strip()
            if content == '{}':
                verify = State.FAILED
            else:
                verify = State.DONE
        return verify

    def analyzestarted():
        before = verified()
        if before == State.FAILED:
            return State.FAILED
        if before == State.WAITING:
            return State.WAITING
        if fastview_result(process):
            return State.DONE
        if before == State.DONE:
            return State.RUNNING
        return State.WAITING

    def fastviewed():
        before = analyzestarted()
        if before == State.FAILED:
            return State.FAILED
        path = fastview_result(process)
        if path is None:
            return State.WAITING
        if os.path.exists(os.path.join(path, 'done')):
            return State.DONE
        if os.path.exists(os.path.join(path, 'failed')):
            return State.FAILED
        if before == State.DONE:
            return State.RUNNING
        return State.WAITING

    def globalviewed():
        before = analyzestarted()
        before_fast = fastviewed()
        if before == State.FAILED or before_fast == State.FAILED:
            return State.FAILED
        path = result_result(process)
        if path is None:
            return State.WAITING
        if os.path.exists(os.path.join(path, 'done')):
            return State.DONE
        if os.path.exists(os.path.join(path, 'failed')):
            return State.FAILED
        if before == State.DONE:
            return State.RUNNING
        return State.WAITING

    def presented():
        before = globalviewed()
        if before == State.FAILED:
            return State.FAILED
        if before == State.DONE:
            if copy_done(process):
                return State.DONE
            return State.RUNNING
        return State.WAITING

    result = Status(
        status=State.RUNNING,
        state=[
            uploaded(),
            verified(),
            analyzestarted(),
            fastviewed(),
            globalviewed(),
            presented()
        ],
        progress=progress,
    )

    if all([item == State.DONE for item in result]):
        result.status = State.DONE
    if any([item == State.RUNNING for item in result]):
        result.status = State.RUNNING  # pylint:disable=redefined-variable-type
    failed = link.failed(process)
    if failed or any([item == State.FAILED for item in result]):
        result.status = State.FAILED
        result.progress = 100
        result.state = [
            item.FAILED if item != State.DONE else item for item in result.state
        ]
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
    ready = viewo.path.ready()
    ready = os.path.join(ready, process)
    todo = viewo.path.todo()
    todo = os.path.join(todo, process)
    path = None
    if os.path.exists(todo):
        path = todo
    # if os.path.exists(ready):
    #     path = ready

    if path is None:
        # invalid process
        return None
    data = os.path.join(path, VERIFY)
    data = utila.file_read(data)
    loaded = json.loads(data)
    return loaded


def result_result(process: str) -> str:
    todo = viewo.path.todo()
    todo = os.path.join(todo, process)
    fastview = os.path.join(todo, 'result')
    if os.path.exists(fastview):
        return fastview
    return None


def copy_done(process: str) -> bool:
    ready = viewo.path.ready()
    ready = os.path.join(ready, process)
    if os.path.exists(ready):
        return True
    return False


def fastview_result(process: str) -> str:
    todo = viewo.path.todo()
    todo = os.path.join(todo, process)
    fastview = os.path.join(todo, FASTVIEW)
    if os.path.exists(fastview):
        return fastview
    return None
