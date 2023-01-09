# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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

import iamraw
import link

FASTVIEW = 'fastview'


@dataclasses.dataclass
class Status:
    status: link.State = link.State.WAITING
    state: 'list[link.State]' = dataclasses.field(default_factory=list)
    progress: int = 0

    def append(self, item):
        self.state.append(item)  # pylint:disable=E1101

    def __getitem__(self, item):
        return self.state[item]  # pylint:disable=E1136


@dataclasses.dataclass
class FastViewGroupStatus:
    title: str = None
    pages: str = None
    error: 'list[str]' = dataclasses.field(default_factory=list)
    good: 'list[str]' = dataclasses.field(default_factory=list)
    warning: 'list[str]' = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class FastViewStatus:

    status: link.State = link.State.RUNNING
    content: 'list[FastViewGroupStatus]' = dataclasses.field(default_factory=list)  # yapf:disable

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


ResultPageViews = 'list[ResultPageView]'  # pylint:disable=C0103
