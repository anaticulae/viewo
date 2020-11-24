# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import http
import json
import json.decoder
import os

import power
import utila
import werkzeug.datastructures

import viewo
import viewo.config

power.setup(viewo.ROOT)

TEST_DATA = os.path.join(viewo.ROOT, 'tests/data')
assert os.path.exists(TEST_DATA), TEST_DATA

BASE_TEMPLATE = utila.file_read(os.path.join(viewo.config.TEMPLATES, 'base.html')) # yapf:disable

TEST_DOCUMENT = 'ework_homework25'
TEST_FINDING = '336248387'

MINIMAL = power.DOCU07_PDF
assert os.path.exists(MINIMAL), MINIMAL

EXAMPLE_READY = power.generated()

EXAMPLE_TODO = os.path.join(TEST_DATA, 'todo')
assert os.path.exists(EXAMPLE_TODO), EXAMPLE_TODO

EXAMPLE_RESULT = os.path.join(EXAMPLE_READY, TEST_DOCUMENT, 'result')

TEST_USER = 'eewuesteewuestee'
TEST_PASSWORD = 'EEWUESTEEWUESTEE'
TEST_EMAIL = 'dertestbaer@helm.com'


@contextlib.contextmanager
def test_user(monkeypatch):
    with monkeypatch.context() as context:

        def verify_password(user: str, password: str) -> bool:
            return user == TEST_USER and password == TEST_PASSWORD

        context.setattr(
            viewo.api.users.data,
            'verify_password',
            verify_password,
        )
        yield


def decode(
        response,
        expected=None,
) -> dict:
    """Read binary data from response and convert them to str"""
    result = response.data.decode('utf8')
    if expected is not None:
        assert response.status_code == expected
    with contextlib.suppress(json.decoder.JSONDecodeError):
        # json format
        return json.loads(result)
    # html format
    return result


def content(
        client,
        request: str,
        expected=http.HTTPStatus.OK,
        raw: bool = False,
):
    response = client.get(request, follow_redirects=True)
    assert response.status_code == expected, request + str(response)
    if raw:
        return response
    return decode(response)


def apicall(
        client,
        request: str,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    cmd = prefix + request
    response = client.get(cmd)
    assert response.status_code == expected, request + str(response)
    return decode(response, expected=expected)


def apidelete(
        client,
        request: str,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    cmd = prefix + request
    response = client.delete(cmd)
    assert response.status_code == expected, request + str(response)
    return decode(response, expected=expected)


def apiupload(
        client,
        page: str,
        field: str,
        path: str,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    """Upload file via http post command"""
    assert field, path
    assert os.path.exists(path), path
    request = prefix + page
    fields = werkzeug.datastructures.MultiDict([(field, open(path, 'rb'))])
    response = client.post(request, data=fields, follow_redirects=True)
    assert response.status_code == expected, request + str(response)
    return decode(response, expected=expected)


def upload(client, file=MINIMAL):
    result = apiupload(
        client,
        '/documents',
        'file',
        file,
    )
    return result


def post(
        client,
        page: str,
        data: dict,
        expected=http.HTTPStatus.OK,
):
    response = client.post(page, data=data, follow_redirects=True)
    assert response.status_code == expected, page
    return decode(response, expected=expected)


def apipost(
        client,
        page: str,
        data: dict,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    request = prefix + page
    return post(client, page=request, data=data, expected=expected)


def apiput(
        client,
        page: str,
        data: dict,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    request = prefix + page
    response = client.put(request, data=data, follow_redirects=True)
    assert response.status_code == expected, request + str(response)
    return decode(response, expected=expected)


def finding_status(client, documentid: str, findingid: int) -> int:
    result = apicall(
        client,
        f'/documents/{documentid}/findings/{findingid}',
        expected=http.HTTPStatus.OK,
    )
    # TODO: UPDATE LATER
    return result['finding']['solution']['status']


def finding_status_update(
        client,
        documentid: str,
        findingid: int,
        status: int,
        expected=http.HTTPStatus.OK,
):
    apiput(
        client,
        f'/documents/{documentid}/findings/{findingid}',
        data={'status': status},
        expected=expected,
    )
