# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import pytest

import tests
import tests.api
import viewo.api.findings.utils


@pytest.mark.usefixtures('findingclient')
def test_api_findings_compare_two_documents_equal():
    compared = viewo.api.findings.utils.compare(
        tests.api.TEST_DOCUMENT,
        tests.api.TEST_DOCUMENT,
    )
    assert compared == []


@pytest.mark.usefixtures('findingclient')
def test_api_findings_compare_two_documents_diff():
    compared = viewo.api.findings.utils.compare(
        tests.api.TEST_DOCUMENT,
        tests.api.TEST_DOCUMENT,
        operation=viewo.api.findings.utils.Comperator.DIFF,
    )
    # TODO: AUTOMATE TEST DATA GENERATOR AND ADD DIFF EXAMPLE
    assert compared == []


def test_api_compare_findings_all(findingclient):
    client = findingclient
    result = tests.apicall(
        client,
        f'/documents/E508AF0DF454GI30/findings/compare/E508AF0DF454GI30',
    )
    assert result['compared']
    assert result['compared']['uri']


def test_api_compare_findings_invalid_partnerid(findingclient):
    client = findingclient
    tests.apicall(
        client,
        f'/documents/E508AF0DF454GI30/findings/compare/INVALIDINVALIDIN',
        expected=http.HTTPStatus.NOT_FOUND,
    )


def test_api_compare_findings_invalid_operation(findingclient):
    client = findingclient
    tests.apicall(
        client,
        f'/documents/E508AF0DF454GI30/findings/compare/E508AF0DF454GI30?operation=invalid',
        expected=http.HTTPStatus.BAD_REQUEST,
    )
