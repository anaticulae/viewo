# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror.finding
import qvlink
import utilo

import viewo.result.update


def update_finding_status(documentid: str, findingid: int, status: int):
    source = qvlink.document(documentid)
    status = viewo.result.update.problem_fromint(status)
    before = protoerror.finding_status(source, findingid)
    if not protoerror.finding_status_update(source, findingid, status):
        utilo.error(f'could not update: {findingid} status: {status}')
        return False
    viewo.result.update.update_bookkeeping(source, status, before)
    return True
