# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
import protocol.finding
import utila
import utilatest
import viewo_api
import werkzeug.datastructures

import viewo
import viewo.config

power.setup(viewo.ROOT)

TEST_DATA = utila.join(viewo.ROOT, 'tests/data', exist=True)

BASE_TEMPLATE = utila.file_read(utila.join(viewo.config.TEMPLATES, 'base.html'))


# TEST_FINDING = '-5427470771429581022'
def first_finding(document) -> int:
    source = utila.join(power.generated(), document)
    for finding in protocol.finding.iter_findings(source):
        first = finding[1][0].number
        return first
    return None


TEST_DOCUMENT = '____home_home025'
TEST_FINDING = first_finding(TEST_DOCUMENT)
INVALID_DOCUMENT = 'rrrrrrrrrrrrrrrr'
INVALID_SECOND = 'SSSSSSSSSSSSSSSS'

MINIMAL = power.DOCU007_PDF
assert os.path.exists(MINIMAL), MINIMAL

EXAMPLE_READY = power.generated()

EXAMPLE_TODO = os.path.join(TEST_DATA, 'todo')
assert os.path.exists(EXAMPLE_TODO), EXAMPLE_TODO

EXAMPLE_ROOT = os.path.join(EXAMPLE_READY, TEST_DOCUMENT)
EXAMPLE_RESULT = os.path.join(EXAMPLE_ROOT, 'result')

TEST_USER = 'eewuesteewuestee'
TEST_PASSWORD = 'EEWUESTEEWUESTEE'  # nosec
TEST_EMAIL = 'dertestbaer@helm.com'


@contextlib.contextmanager
def test_user(monkeypatch):
    with monkeypatch.context() as context:

        def password_verify(user: str, password: str) -> bool:
            return user == TEST_USER and password == TEST_PASSWORD

        context.setattr(
            viewo_api,
            'password_verify',
            password_verify,
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


def upload(client, file=MINIMAL):
    result = utilatest.apiupload(
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
    assert response.status_code == expected, f'path: {page}, error: {response.status_code}'
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
    result = utilatest.apicall(
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
