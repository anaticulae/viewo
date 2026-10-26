# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import copy
import os
import threading
import time

import configos
import iamraw
import link
import protocol
import utilo

import viewo.result.json

FRONTEND_SAVER_WAIT = configos.HV_INT_PLUS(default=50)


class FindingsFrontEnd:

    def __init__(self, documentid: str, path: str):
        self.documentid = documentid
        self.path = path
        self.loaded = None
        self.fast = {}
        self.outdated = False
        utilo.debug(f'create FindingFrontEnd: {documentid}')

    def update_status(self, findingid: int, status: iamraw.ProblemStatus):
        assert isinstance(status, iamraw.ProblemStatus), type(status)
        try:
            self.fast[findingid].solution.status = status
        except KeyError:
            return False
        self.outdated = True
        return True

    def findings(self, pages: tuple = None, status=None):
        if self.loaded is None:
            self.load()
        data = list(self.loaded)
        if pages is not None:
            data = utilo.select_pages(data, pages=pages)
        data = utilo.notnone(data)
        for page in data:
            # remove not selected items
            page.content = [
                finding for finding in page.content if status is None or
                (finding.solution and finding.solution.status == status)
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
        self.fast = {
            item.number: item for item in utilo.flatten_content(findings)
        }
        self.loaded = findings

    def save(self):
        utilo.log(f'write updated findings to: {self.path}')
        findings = utilo.flatten_content(self.loaded)  # TODO: REMOVE LATER
        private = link.private(
            self.documentid,
            done=True,
        )
        protocol.write_grouped(findings, self.path, private=private)
        link.update_bookkeeping(self.documentid)
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
        self.saver = None

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

    def run_saveme(self):
        utilo.log('start saving scheduler')
        while True:  # pylint:disable=W0149
            for item in self.documents.values():
                if not item.outdated:
                    continue
                # write current state to hdd
                try:
                    item.save()
                except Exception as error:  # pylint:disable=broad-except
                    utilo.error('could not save findings')
                    utilo.print_stacktrace()
                    utilo.error(error)
            time.sleep(FRONTEND_SAVER_WAIT)
            utilo.debug('wait for saving')

    def start(self):
        if self.saver is not None:
            utilo.error('scheduler is already started')
            return
        if utilo.testing():
            utilo.debug('testing requires no scheduler')
            return
        # scheduler is not required in test run TODO: VERIFY THIS
        self.saver = threading.Thread(target=self.run_saveme)
        self.saver.start()


FRONTEND = FrontEndCollection()

start = FRONTEND.start  # pylint:disable=C0103


def frontend(documentid: str) -> FindingsFrontEnd:
    return FRONTEND[documentid]


def convert_style_markup(findings: iamraw.PageFindings) -> iamraw.PageFindings:
    for finding in findings.content:
        finding.solution.description = viewo.result.json.message_replace(
            finding.solution.description)
    return findings
