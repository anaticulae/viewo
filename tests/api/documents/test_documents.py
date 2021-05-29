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


def test_api_documents_overview(client):
    result = tests.apicall(client, '/documents')
    assert not result['documents']

    tests.apiupload(client, '/documents', 'file', tests.MINIMAL)

    result = tests.apicall(client, '/documents')
    assert result['documents']


def test_api_document_get_no_resource(client):
    result = tests.apicall(
        client,
        '/documents/invalid_document',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'not found' in result['error']


def test_api_document_get_byid(client):
    result = tests.apiupload(client, '/documents', 'file', tests.MINIMAL)
    tests.api.login(
        client,
        userid=result['userid'],
        password=result['password'],
    )
    result = tests.apicall(
        client,
        result['document'],
        prefix='',
    )
    assert result['document']['title']


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
        '/documents/invalid_document',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'error' in result


def test_api_documents_links(findingclient):
    result = tests.apicall(findingclient, '/documents/master_master075/links')
    assert result['links']
    assert len(result['links']['resource']) >= 10
