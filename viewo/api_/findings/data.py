# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import copy
import os

import flask
import iamraw
import link
import protocol
import utila

import viewo.result.json


class FindingsFrontEnd:

    def __init__(self, documentid: str, path: str):
        self.documentid = documentid
        self.path = path
        self.loaded = None
        self.fast = {}
        self.outdated = False

    def update_status(self, findingid: int, status: iamraw.ProblemStatus):
        assert isinstance(status, iamraw.ProblemStatus), type(status)
        try:
            self.fast[findingid].solution.status = status
        except KeyError:
            return False
        self.outdated = True
        return True

    def findings(self, pages: tuple = None, status=iamraw.ProblemStatus.OPEN):
        if self.loaded is None:
            self.load()
        data = list(self.loaded)
        if pages is not None:
            data = utila.select_pages(data, pages=pages)
        data = utila.notnone(data)
        for page in data:
            # remove not selected items
            page.content = [
                finding for finding in page.content if status is None or
                finding.solution and finding.solution.status == status
            ]
        data = sorted(data, key=lambda x: x.page)
        data = copy.deepcopy(data)
        return data

    def fastfindings(self, pages: tuple = None, status=None):
        if self.loaded is None:
            self.load()
        data = self.findings(pages=pages, status=status)
        for page in data:
            page.content = [finding.number for finding in page.content]
        return data

    def load(self):
        findings = protocol.load_grouped(self.path)
        findings = [convert_style_markup(page) for page in findings]
        self.loaded = findings
        self.fast = {
            item.number: item for item in utila.flatten_content(self.loaded)
        }

    def save(self):
        findings = utila.flatten_content(self.loaded)  # TODO: REMOVE LATER
        protocol.write_grouped(findings, self.path)
        self.outdated = False

    def __getitem__(self, key):
        key = int(key)
        if self.loaded is None:
            self.load()
        copied = copy.deepcopy(self.fast[key])
        return copied


class FrontEndCollection:

    def __init__(self):
        self.documents = {}

    def __getitem__(self, documentid) -> FindingsFrontEnd:
        try:
            return self.documents[documentid]
        except KeyError as error:
            optimizedpath = link.optimized(documentid, done=True)
            if not os.path.exists(optimizedpath):
                raise error
        loaded = FindingsFrontEnd(documentid=documentid, path=optimizedpath)
        self.documents[documentid] = loaded
        return loaded


def frontend(documentid: str) -> FindingsFrontEnd:
    collection = getattr(flask.g, '_findings', None)
    if collection is None:
        collection = flask.g._findings = FrontEndCollection()
    return collection[documentid]


def convert_style_markup(findings: iamraw.PageFinding) -> iamraw.PageFinding:
    for finding in findings.content:
        finding.solution.description = viewo.result.json.message_replace(
            finding.solution.description)
    return findings
