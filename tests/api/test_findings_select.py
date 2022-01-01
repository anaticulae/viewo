# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import utilatest

import tests


def test_api_findings_bypagenumber(findingclient):
    client = findingclient
    result = utilatest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings?pages=0:5',
        expected=http.HTTPStatus.OK,
    )
    expected = f'documents/{tests.TEST_DOCUMENT}/findings?pages=0%3A5'
    assert expected in result['findings']['uri']


def test_api_findings_negative_pagenumber(findingclient):
    """Collect findings of page -3 till page 5."""
    client = findingclient
    result = utilatest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings?pages=_3:5',
        expected=http.HTTPStatus.OK,
    )
    expected = f'documents/{tests.TEST_DOCUMENT}/findings?pages=_3%3A5'
    assert expected in result['findings']['uri']
