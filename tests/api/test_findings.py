# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import pytest
import utilotest

import tests


def test_api_findings_overview_bydocumentid(findingclient):
    client = findingclient
    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings',
    )
    assert result['findings']
    assert result['findings']['uri']


def test_api_fastfindings_bydocumentid(findingclient):
    client = findingclient
    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/fastfindings',
    )
    assert 18 <= len(result) <= 25


def test_api_findings_pages_outranges(findingclient):
    """Upper page mark outranges valid pages(18). Request is cutted at
    top page border."""
    client = findingclient
    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/fastfindings?pages=15:50',
    )
    assert 5 <= len(result) < 10


def test_api_findings_overview_by_invalid_documentid(client):
    utilotest.apicall(
        client,
        '/documents/invalid_document/findings',
        expected=http.HTTPStatus.NOT_FOUND,
    )


def test_api_findings_byfindingid_notexists(docclient):
    client, doc = docclient
    utilotest.get(
        client,
        f'{doc}/findings/notexists',
        expected=http.HTTPStatus.NOT_FOUND,
    )


@pytest.mark.skipif(not tests.TEST_FINDING, reason='generate resources')
def test_api_findings_byfindingid(findingclient):
    client = findingclient
    result = utilotest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings/{tests.TEST_FINDING}',
        expected=http.HTTPStatus.OK,
    )
    assert result['finding']['uri']


@pytest.mark.skipif(not tests.TEST_FINDING, reason='generate resources')
def test_api_finding_solve_valid(findingclient):
    client = findingclient

    tests.finding_status_update(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
        status=4,
    )
    status = tests.finding_status(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
    )
    assert status == 4

    tests.finding_status_update(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
        status=0,
    )
    status = tests.finding_status(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
    )
    assert status == 1

    tests.finding_status_update(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
        status=4,
    )
    status = tests.finding_status(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
    )
    assert status == 4

    tests.finding_status_update(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
        status=1,
    )
    status = tests.finding_status(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
    )
    assert status == 1


@pytest.mark.skipif(not tests.TEST_FINDING, reason='generate resources')
def test_api_finding_solve_invalid(findingclient):
    client = findingclient
    tests.finding_status_update(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
        status=10,  # out of range
        expected=http.HTTPStatus.BAD_REQUEST,
    )
    status = tests.finding_status(
        client,
        tests.TEST_DOCUMENT,
        tests.TEST_FINDING,
    )
    assert status == 1
