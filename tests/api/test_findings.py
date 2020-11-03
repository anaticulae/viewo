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


def test_api_findings_overview_bydocumentid(findingclient):
    client = findingclient
    result = tests.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings',
    )
    assert result['findings']
    assert result['findings']['uri']


def test_api_findings_overview_by_invalid_documentid(client):
    tests.apicall(
        client,
        '/documents/invalid_document/findings',
        expected=http.HTTPStatus.NOT_FOUND,
    )


def test_api_findings_byfindingid_notexists(docclient):
    client, doc = docclient
    tests.apicall(
        client,
        f'{doc}/findings/notexists',
        prefix='',
        expected=http.HTTPStatus.NOT_FOUND,
    )


def test_api_findings_byfindingid(findingclient):
    client = findingclient
    result = tests.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings/{tests.TEST_FINDING}',
        expected=http.HTTPStatus.OK,
    )
    assert result['finding']['uri']


def test_api_finding_solve(findingclient):
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
