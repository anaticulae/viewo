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

TEST_DOCUMENT = 'ework_homework25'


def test_api_pages_overview(findingclient):
    client = findingclient
    result = tests.apicall(
        client,
        f'/documents/{TEST_DOCUMENT}/pages',
    )
    assert result['pages']
    assert result['pages']['uri']


def test_api_pages_overview_range(findingclient):
    client = findingclient
    result = tests.apicall(
        client,
        f'/documents/{TEST_DOCUMENT}/pages?range=1',
    )
    assert result['pages']
    assert result['pages']['uri']
    assert len(result['pages']['html']) == 1

    result = tests.apicall(
        client,
        f'/documents/{TEST_DOCUMENT}/pages?range=0:3',
    )
    assert len(result['pages']['html']) == 3


def test_api_pages_overview_invalid_range(findingclient):
    client = findingclient
    tests.apicall(
        client,
        f'/documents/{TEST_DOCUMENT}/pages?range=0:xxx-10:-50',
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_pages_overview_invalid_document(findingclient):
    client = findingclient
    tests.apicall(
        client,
        f'/documents/invalid_document/pages',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    tests.apicall(
        client,
        f'/documents/invalid_document/pages?range=0:xxx-10:-50',
        expected=http.HTTPStatus.NOT_FOUND,
    )
