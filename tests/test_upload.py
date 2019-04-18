# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from http import HTTPStatus
from os import listdir
from os.path import exists
from tests import MINIMAL
from tests import result
from tests import todo

import flask
from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import MultiDict

from viewo.upload import upload_pdf


def todo_count(app) -> int:
    """Count files ?and FOLDER? in common `todo` folder"""
    return len(listdir(todo(app)))


def post_file(client, page: str, field: str, path: str):
    """Upload file via http post command"""
    assert field, path
    assert exists(path), path
    fields = MultiDict([(field, open(path, 'rb'))])
    response = client.post(
        page,
        data=fields,
        follow_redirects=True,
    )
    return response


UPLOAD_PATH = '/upload'
DOCUMENT_PATH = '/documents'


def test_upload(client, app):
    """Upload one file and check if it is saved at common todo folder"""
    # test that viewing the page renders without template errors
    assert client.get('/').status_code == HTTPStatus.OK

    # count files in todo folder
    files_before = todo_count(app)

    response = post_file(client, page=UPLOAD_PATH, field='file', path=MINIMAL)
    assert response.status_code == HTTPStatus.OK

    files_after = todo_count(app)

    # check if file was uploaded
    assert files_after == files_before + 1


def test_upload_with_wrong_field(client, app):
    """Upload one file and check if it is saved at common todo folder"""
    # test that viewing the page renders without template errors
    assert client.get('/').status_code == HTTPStatus.OK

    # count files in todo folder
    files_before = todo_count(app)

    # Upload with wrong field
    response = post_file(client, page=UPLOAD_PATH, field='o_o', path=MINIMAL)
    assert response.status_code == HTTPStatus.OK
    assert 'Fehler' in result(response)
    files_after = todo_count(app)
    # check that no file was uploaded
    assert files_after == files_before


def test_upload_get_forward_to_documents(client):
    response = client.get(UPLOAD_PATH)

    location = response.headers['Location']

    assert DOCUMENT_PATH in location
    assert response.status_code == HTTPStatus.FOUND


# def test_upload_without_filename(monkeypatch, client, app):

#     class MyRequest:
#         pass

#     with monkeypatch.context() as context:
#         # Remove all environment vars
#         my_request = MyRequest()
#         my_request.method = 'POST'
#         empty_file = MyRequest()
#         empty_file.filename = ''
#         my_request.files = {'file': empty_file}
#         context.setattr(flask.globals, 'request', my_request)
#         # context.setattr(flask.globals, 'top', [1])
#         upload_pdf()
