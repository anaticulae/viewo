# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http
import os

import link
import power
import pytest
import utila
import werkzeug.datastructures

import tests


def post_file(client, page: str, field: str, path: str):
    """Upload file via http post command"""
    assert field, path
    assert os.path.exists(path), path
    fields = werkzeug.datastructures.MultiDict([(field, open(path, 'rb'))])
    response = client.post(
        page,
        data=fields,
        follow_redirects=True,
    )
    return response


UPLOAD_PATH = '/upload'
DOCUMENT_PATH = '/documents'


def test_upload(client):
    """Upload one file and check if it is saved at common todo folder"""
    # test that viewing the page renders without template errors
    assert client.get('/').status_code == http.HTTPStatus.OK

    # count files in todo folder
    files_before = link.count_todo()

    response = post_file(
        client,
        page=UPLOAD_PATH,
        field='file',
        path=tests.MINIMAL,
    )
    assert response.status_code == http.HTTPStatus.OK

    files_after = link.count_todo()

    # check if file was uploaded
    assert files_after == files_before + 1


def test_upload_with_wrong_field(client):
    """Upload one file and check if it is saved at common todo folder"""
    # test that viewing the page renders without template errors
    assert client.get('/').status_code == http.HTTPStatus.OK

    # count files in todo folder
    files_before = link.count_todo()

    # Upload with wrong field
    response = post_file(
        client,
        page=UPLOAD_PATH,
        field='o_o',
        path=tests.MINIMAL,
    )
    assert response.status_code == http.HTTPStatus.OK
    assert 'Fehler' in tests.decode(response)
    files_after = link.count_todo()
    # check that no file was uploaded
    assert files_after == files_before


def test_upload_get_forward_to_documents(client):
    response = client.get(UPLOAD_PATH)

    location = response.headers['Location']

    assert DOCUMENT_PATH in location
    assert response.status_code == http.HTTPStatus.FOUND


def upload(client, source: str, valid: bool = True):
    # test that viewing the page renders without template errors
    assert client.get('/').status_code == http.HTTPStatus.OK

    # count files in todo folder
    files_before = link.count_todo()

    fields = werkzeug.datastructures.MultiDict([('url', source)])
    response = client.post(UPLOAD_PATH, data=fields, follow_redirects=True)

    assert response.status_code == http.HTTPStatus.OK

    files_after = link.count_todo()

    # check if file was uploaded
    assert files_after == (files_before + 1 if valid else files_before)


def test_upload_from_url(client):
    source = f'file:///{utila.forward_slash(power.MASTER072_PDF)}'
    upload(client, source)


@pytest.mark.parametrize('source', [
    pytest.param('http://invalid.dscom', id='invalid url'),
    pytest.param(f'file:///{__file__}', id='no pdf'),
])
def test_upload_from_url_with_error(source, client):
    upload(client, source, valid=False)


def test_upload_from_url_too_large_file(client, testdir):
    content = b'%PDF-1.5' + b'0' * 1024 * 1024 * 100  # 100 MB
    pdf = str(os.path.join(testdir.tmpdir, 'upload.pdf'))
    utila.file_create_binary(pdf, content)
    source = f'file:///{pdf}'

    upload(client, source, valid=False)
