# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http
import os

import power
import pytest
import utila

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
        '/documents/abc',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'not found' in result['error']


def test_api_document_get_byid(client):
    result = tests.apiupload(client, '/documents', 'file', tests.MINIMAL)
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
        '/documents/abc',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert 'error' in result


def test_api_upload_document(client):
    result = tests.apiupload(client, '/documents', 'file', tests.MINIMAL)
    assert result['document']
    assert result['link']


def test_api_upload_from_url(client):
    source = f'file:///{utila.forward_slash(power.MASTER072_PDF)}'
    result = tests.apipost(client, '/documents', data={'url': source})
    assert result['document']


@pytest.mark.parametrize('source, expected_error', [
    pytest.param('http://invalid.dscom', 'invalid url', id='invalid url'),
    pytest.param(f'file:///{__file__}', 'require pdf', id='no pdf'),
])
def test_api_upload_from_url_with_error(source, client, expected_error):
    result = tests.apipost(
        client,
        '/documents',
        data={'url': source},
        expected=http.HTTPStatus.BAD_REQUEST,
    )
    assert expected_error in result['message']


def test_api_upload_from_url_too_large_file(client, testdir):
    content = b'%PDF-1.5' + b'0' * 1024 * 1024 * 100  # 100 MB
    pdf = str(os.path.join(testdir.tmpdir, 'upload.pdf'))
    utila.file_create_binary(pdf, content)
    source = f'file:///{pdf}'
    tests.apipost(
        client,
        page='/documents',
        data={'url': source},
        expected=http.HTTPStatus.BAD_REQUEST,
    )
