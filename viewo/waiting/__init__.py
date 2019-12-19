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
import typing

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


@dataclasses.dataclass
class FastViewGroupStatus:
    title: str = None
    pages: str = None
    error: typing.List[str] = dataclasses.field(default_factory=list)
    good: typing.List[str] = dataclasses.field(default_factory=list)
    warning: typing.List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class FastViewStatus:

    status: typing.List[FastViewGroupStatus] = \
                                        dataclasses.field(default_factory=list)

    def __len__(self):
        return len(self.status)

    def __getitem__(self, index):
        return self.status[index]  # pylint:disable=E1136

    def append(self, item):
        return self.status.append(item)
