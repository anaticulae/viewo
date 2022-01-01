# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import pytest
import utilatest

import tests
import tests.api
import viewo.api_.findings.compare


@pytest.mark.usefixtures('findingclient')
def test_api_findings_compare_two_documents_equal():
    compared = viewo.api_.findings.compare.compare(
        tests.TEST_DOCUMENT,
        tests.TEST_DOCUMENT,
    )
    assert compared == []


@pytest.mark.usefixtures('findingclient')
def test_api_findings_compare_two_documents_diff():
    compared = viewo.api_.findings.compare.compare(
        tests.TEST_DOCUMENT,
        tests.TEST_DOCUMENT,
        operation=viewo.api_.findings.compare.Comperator.DIFF,
    )
    # TODO: AUTOMATE TEST DATA GENERATOR AND ADD DIFF EXAMPLE
    assert compared == []


def test_api_compare_findings_all(findingclient):
    client = findingclient
    result = utilatest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings/compare/{tests.TEST_DOCUMENT}',
    )
    assert result['compared']
    assert result['compared']['uri']


def test_api_compare_findings_invalid_partnerid(findingclient):
    client = findingclient
    utilatest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings/compare/INVALIDINVALIDIN',
        expected=http.HTTPStatus.NOT_FOUND,
    )


def test_api_compare_findings_invalid_operation(findingclient):
    client = findingclient
    utilatest.apicall(
        client,
        f'/documents/{tests.TEST_DOCUMENT}/findings/compare/{tests.TEST_DOCUMENT}?operation=invalid',
        expected=http.HTTPStatus.BAD_REQUEST,
    )


@pytest.mark.usefixtures('findingclient')
def test_api_findings_compare_non_existing():
    """Invoke comparison with two non existing documentid's."""
    compared = viewo.api_.findings.compare.compare(
        tests.INVALID_DOCUMENT,
        tests.INVALID_SECOND,
    )
    assert compared is None  # pylint:disable=C2001
