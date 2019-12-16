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
import typing


class State(enum.Enum):
    waiting = -1
    done = 0
    running = 1
    failed = 2


@dataclasses.dataclass
class Status:
    status: State = State.waiting
    state: typing.List[State] = dataclasses.field(default_factory=list)


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
