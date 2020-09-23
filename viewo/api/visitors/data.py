# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import os

import utila

import viewo.config


@dataclasses.dataclass(unsafe_hash=True)
class Visit:
    unique: str = None
    date: str = None
    call: str = None


def append(visit: Visit):
    assert visit, str(visit)
    outpath = os.path.join(viewo.config.VISITORS, str(visit.unique))
    raw = raw_visit(visit) + utila.NEWLINE
    utila.file_append(outpath, raw, create=True)


def raw_visit(visit: Visit) -> str:
    return f'{visit.date} {visit.call}'
