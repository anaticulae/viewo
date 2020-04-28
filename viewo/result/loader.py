# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import protocol


def load_findings(path: str) -> dict:
    assert os.path.exists(path), str(path)
    # TODO: REPLACE WITH LOAD FINDING METHOD FROM PROTOCOL
    files = [item for item in os.listdir(path) if item.endswith('.yaml')]

    findings = []
    for item in files:
        loaded = protocol.load_result(os.path.join(path, item))
        findings.extend(loaded)

    # TODO: unite with feedback enumerater
    for index, finding in enumerate(findings):
        finding.number = index

    grouped = {page.page: page for page in protocol.bylocation(findings)}
    return grouped
