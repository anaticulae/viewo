# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import link

import tests


def test_api_upload_document(client):
    result = tests.apiupload(client, '/documents', 'file', tests.MINIMAL)
    assert result['document']
    assert result['link']


def test_api_upload_document_wrong_datatype(client):
    tests.apiupload(
        client,
        '/documents',
        'file',
        __file__,
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_upload_with_wrong_field(client):
    """Upload one file and check if it is saved at common todo folder"""
    # test that viewing the page renders without template errors
    assert client.get('/').status_code == http.HTTPStatus.OK

    # count files in todo folder
    files_before = link.count_todo()

    # Upload with wrong field
    tests.apiupload(
        client,
        page='/documents',
        field='o_o',
        path=tests.MINIMAL,
        expected=http.HTTPStatus.BAD_REQUEST,
    )
    files_after = link.count_todo()
    # check that no file was uploaded
    assert files_after == files_before
