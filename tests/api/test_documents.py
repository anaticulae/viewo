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


def test_api_documents_overview(client):
    result = tests.apicall(client, '/documents')
    assert not result['documents']


def test_api_document_byid(client):
    result = tests.apicall(
        client,
        '/documents/abc',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'not found' in result['error']
