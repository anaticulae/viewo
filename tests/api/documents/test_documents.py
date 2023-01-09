# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import utilatest

import tests


def test_api_documents_overview(client):
    result = utilatest.apicall(client, '/documents')
    assert not result['documents']
    utilatest.apiupload(client, '/documents', 'file', tests.MINIMAL)
    result = utilatest.apicall(client, '/documents')
    assert result['documents']


def test_api_document_get_no_resource(client):
    result = utilatest.apicall(
        client,
        '/documents/invalid_document',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'not found' in result['error']


def test_api_document_get_byid(client):
    result = utilatest.apiupload(client, '/documents', 'file', tests.MINIMAL)
    tests.api.login(
        client,
        userid=result['userid'],
        password=result['password'],
    )
    result = utilatest.get(
        client,
        result['document'],
    )
    assert result['document']['title']


def test_api_delete_document_byid(client):
    result = tests.upload(client, file=tests.MINIMAL)
    created = result['document']
    # delete pdf file with `DELETE {resource_path}`
    result = utilatest.delete(
        client,
        request=created,
    )
    # delete it again will produce BAD_REQUEST answer
    result = utilatest.delete(
        client,
        request=created,
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_delete_document_which_does_not_exists(client):
    result = utilatest.apidelete(
        client,
        '/documents/invalid_document',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'error' in result


def test_api_documents_links(findingclient):
    result = utilatest.apicall(findingclient,
                               '/documents/master_master075/links')
    assert result['links']
    assert len(result['links']['resource']) >= 10
