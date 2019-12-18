# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Waiting room
============

This is the waiting room. After submitting the thesis, the user waits in
the waiting room that document is processed.

There are two views which delivers results:
  * Fast view
  * General view

Fast view
---------

    the feedback is generated in less than 5 seconds

General view
------------

    test

Waiting view
------------

* Empfange Dokument
* Validiere empfangenes Dokument
* Starte Analyse
* Schnelldurchsicht
* Gesamtdurchsicht
* Praesentiere Gesamtergebnis

"""
import dataclasses
import enum
import json
import os
import typing

import configo
import flask
import utila

waiting_ = flask.Blueprint('waiting', __name__)  # pylint:disable=C0103

VERIFY = 'pdfinfo.json'


class State(enum.Enum):
    waiting = -1
    done = 0
    running = 1
    failed = 2

    @staticmethod
    def fromstr(item: str):
        # TODO: DIRTY, replace
        item = int(item)
        for state in State:
            if state.value == item:
                return state
        return None


@dataclasses.dataclass
class Status:
    status: State = State.waiting
    state: typing.List[State] = dataclasses.field(default_factory=list)

    def append(self, item):
        self.state.append(item)  # pylint:disable=E1101

    def __getitem__(self, item):
        return self.state[item]  # pylint:disable=E1136


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


def loads(content: str) -> Status:
    loaded = json.loads(content)
    result = Status()
    result.status = State.fromstr(loaded['status'])
    for item in loaded['states']:
        parsed = State.fromstr(item)
        result.append(parsed)  # pylint:disable=E1101
    return result


@waiting_.route('/waiting/<string:process>')
def waiting_view(process):
    return flask.render_template('waiting.html', process=process)


@waiting_.route('/waiting/validation', defaults={'process': None})
@waiting_.route('/waiting/validation/<string:process>')
def waiting_view_validation(process):
    if process is None:
        return flask.redirect(flask.url_for('result.failure'))
    rendered = flask.render_template(
        'waiting_validation.html',
        process=process,
    )
    return rendered


@waiting_.route('/waiting/status/<string:process>')
def waiting_status(process):
    try:
        process = str(process)
    except UnicodeDecodeError:
        return '{}'
    if not process:
        return '{}'
    loaded = status(process)
    if not loaded:
        return '{}'
    dumped = jsonify(loaded)
    return dumped


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
        if before == State.done:
            return State.running
        return State.waiting

    def fastviewed():
        before = analyzestarted()
        if before == State.failed:
            return State.failed
        return State.waiting

    def globalviewed():
        before = analyzestarted()
        before_fast = fastviewed()
        if before == State.failed or before_fast == State.failed:
            return State.failed
        return State.waiting

    def presented():
        before = globalviewed()
        if before == State.failed:
            return State.failed
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
