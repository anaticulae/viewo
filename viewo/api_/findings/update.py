# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import protocol.finding
import utila

import viewo.result.update


def update_finding_status(documentid: str, findingid: int, status: int):
    source = link.document(documentid)
    status = viewo.result.update.problem_fromint(status)
    before = protocol.finding_status(source, findingid)
    if not protocol.finding_status_update(source, findingid, status):
        utila.error(f'could not update: {findingid} status: {status}')
        return False
    viewo.result.update.update_bookkeeping(source, status, before)
    return True
