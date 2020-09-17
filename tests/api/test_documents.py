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
import tests.api


def test_api_documents_overview(client):
    result = tests.apicall(client, '/documents')
    assert not result['documents']


def test_api_document_get(client):
    result = tests.apicall(
        client,
        '/documents/abc',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'not found' in result['error']


def test_api_delete_document_byid(client):
    result = tests.upload(client, file=tests.MINIMAL)
    created = result['document']
    # delete pdf file with `DELETE {resource_path}`
    result = tests.apidelete(client, request=created, prefix='')
    # delete it again will produce BAD_REQUEST answer
    result = tests.apidelete(
        client,
        request=created,
        prefix='',
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_delete_document_which_does_not_exists(client):
    result = tests.apidelete(
        client,
        '/documents/abc',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'error' in result


def test_api_upload_document(client):
    result = tests.apiupload(
        client,
        '/documents',
        'file',
        tests.MINIMAL,
    )
    assert result['document']
    assert result['link']
