# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import link
import utilo


def update_bookkeeping(
    source: str,
    status: iamraw.ProblemStatus,
    before: iamraw.ProblemStatus,
):
    jobpath = os.path.join(source, link.JOB_FILE_NAME)
    loaded = link.load_job(jobpath)
    # update BOOKKEEPING
    if status == iamraw.ProblemStatus.SOLVED:
        # solved
        updated = link.FindingStatus(
            loaded.result.open - 1,
            loaded.result.closed + 1,
            loaded.result.excluded,
        )
    elif status == iamraw.ProblemStatus.DISAGREE:
        # removed
        updated = link.FindingStatus(
            loaded.result.open - 1,
            loaded.result.closed,
            loaded.result.excluded + 1,
        )
    elif status == iamraw.ProblemStatus.OPEN:
        # open
        solved = before == iamraw.ProblemStatus.SOLVED
        deleted = before == iamraw.ProblemStatus.DISAGREE
        # yapf:disable
        updated = link.FindingStatus(
            loaded.result.open + 1,
            loaded.result.closed if not solved else loaded.result.closed - 1,
            loaded.result.excluded if not deleted else loaded.result.excluded - 1,
        )
        # yapf:enable
    else:
        utilo.error(f'status: {status} not supported - {source}')
        return
    loaded.result = updated
    dumped = link.dump_job(loaded)
    utilo.file_replace(jobpath, dumped)


def problem_fromint(status: int) -> iamraw.ProblemStatus:
    if status in {0, 1}:
        return iamraw.ProblemStatus.OPEN
    if status == 4:
        return iamraw.ProblemStatus.SOLVED
    return iamraw.ProblemStatus.DISAGREE
