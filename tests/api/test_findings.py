# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import tests


def test_api_findings_overview_bydocumentid(docclient):
    client, doc = docclient
    result = tests.apicall(
        client,
        f'{doc}/findings',
        prefix='',
    )
    assert not result['findings']


def test_api_findings_overview_by_invalid_documentid(client):
    tests.apicall(
        client,
        '/documents/invalid_documentid/findings',
        expected=http.HTTPStatus.NOT_FOUND,
    )
