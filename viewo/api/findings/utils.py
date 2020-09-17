# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import protocol


def all_findings(documentid: str):
    documentpath = link.document(documentid)  # pylint:disable=E1101
    if documentpath is None:
        return None
    findings = protocol.findings_from_path(documentpath)
    return findings
