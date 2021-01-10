# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import tests


def test_api_findings_bypagenumber(findingclient):
    client = findingclient
    result = tests.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings?pages=0:5',
        expected=http.HTTPStatus.OK,
    )
    expected = f'documents/{tests.TEST_DOCUMENT}/findings?pages=0%3A5'
    assert expected in result['findings']['uri']
