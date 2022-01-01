# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import contextlib
import enum
import typing

import link
import protocol
import utila

import viewo.api.utils

ComparedFinding = collections.namedtuple(
    'ComparedFinding',
    'page, current, other',
)
ComparedListFinding = typing.List[ComparedFinding]


class Comperator(enum.Enum):
    ALL = enum.auto()
    EQUAL = enum.auto()
    DIFF = enum.auto()


def compare(
    documentid: str,
    partnerid: str,
    operation: Comperator = Comperator.ALL,
) -> ComparedListFinding:
    documentpath = link.optimized(documentid, done=True)
    if not utila.exists(documentpath):
        return None
    partnerpath = link.optimized(partnerid, done=True)
    if not utila.exists(partnerpath):
        return None
    if documentid == partnerid:
        # equal documents
        return []
    document = protocol.load_grouped(documentpath)
    partner = protocol.load_grouped(partnerpath)
    compared = []
    for number, content in utila.sync_pages((document, partner)):
        left = content[0] if content[0] else []
        right = content[1] if content[1] else []
        # run selected filter
        if operation == Comperator.EQUAL:
            left = [finding for finding in left if finding in right]
        elif operation == Comperator.DIFF:
            # TODO: IS THIS DIFF BEHAVIOR USEFUL/SENSEFUL?
            left, right = (
                [finding for finding in left if finding not in right],
                [finding for finding in right if finding not in left],
            )
        current = ComparedFinding(number, left, right)
        compared.append(current)
    return compared


def compare_raw(pages: ComparedListFinding):
    result = []
    for page in pages:
        raw = {
            'page': page.page,
            'current': utila.simplify(page.current),
            'other': utila.simplify(page.other),
        }
        result.append(raw)
    return result


def comperator_fromraw(raw: str) -> Comperator:
    raw = raw.upper()
    with contextlib.suppress(KeyError):
        return viewo.api_.findings.compare.Comperator[raw]
    return None
