# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import utilotest

import tests


def test_api_pages_overview(findingclient):
    client = findingclient
    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/pageviews',
    )
    assert result['pageviews']
    assert result['pageviews']['uri']


def test_api_pages_overview_range(findingclient):
    client = findingclient
    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/pageviews?pages=1',
    )
    assert result['pageviews']
    assert result['pageviews']['uri']
    assert len(result['pageviews']['html']) == 1

    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/pageviews?pages=0:3',
    )
    assert len(result['pageviews']['html']) == 3


def test_api_pages_overview_invalid_range(findingclient):
    client = findingclient
    utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/pageviews?pages=0:xxx-10:-50',
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_pages_overview_invalid_document(findingclient):
    client = findingclient
    utilotest.apicall(
        client,
        '/documents/invalid_document/pageviews',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    utilotest.apicall(
        client,
        '/documents/invalid_document/pageviews?pages=0:xxx-10:-50',
        expected=http.HTTPStatus.NOT_FOUND,
    )


def test_api_pages_pagenumbers(findingclient):
    client = findingclient
    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/pagenumbers',
    )
    pagenumbers = result['pagenumbers']['resource']
    assert len(pagenumbers) == 25
