# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
* Präsentiere Gesamtergebnis

"""

import contextlib
import dataclasses
import enum
import typing

import iamraw

VERIFY = 'pdfinfo.json'
FASTVIEW = 'fastview'


class State(enum.Enum):
    WAITING = -1
    DONE = 0
    RUNNING = 1
    FAILED = 2

    @staticmethod
    def fromstr(item: str):
        with contextlib.suppress(ValueError):
            item = int(item)
        for state in State:
            if state.value == item:
                return state
        raise ValueError(f'could not create State from `{item}`')


@dataclasses.dataclass
class Status:
    status: State = State.WAITING
    state: typing.List[State] = dataclasses.field(default_factory=list)
    progress: int = 0

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

    status: State = State.RUNNING
    content: typing.List[FastViewGroupStatus] = \
                                        dataclasses.field(default_factory=list)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136

    def append(self, item):
        return self.content.append(item)  # pylint:disable=E1101


@dataclasses.dataclass
class ResultPageView:
    page: int = None
    html: str = None
    findings: iamraw.Findings = dataclasses.field(default_factory=list)

    def __len__(self):
        return len(self.findings)

    def __getitem__(self, index):
        return self.findings[index]  # pylint:disable=E1136

    def append(self, item):
        return self.findings.append(item)  # pylint:disable=E1101


ResultPageViews = typing.List[ResultPageView]
