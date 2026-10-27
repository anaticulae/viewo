# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import http
import json
import json.decoder
import os

import hoverpower
import protoerror.finding
import pytest
import utilo
import utilotest
import viewo_api
import werkzeug.datastructures

import viewo
import viewo.config

hoverpower.setup(viewo.ROOT)

BASE_TEMPLATE = utilo.file_read(utilo.join(viewo.config.TEMPLATES, 'base.html'))

run, fail = utilotest.create_cli_runner(viewo)


# TEST_FINDING = '-5427470771429581022'
def first_finding(document) -> int:
    source = utilo.join(hoverpower.generated(folder='ready'), document)
    if not utilo.exists(source):
        utilo.error('run resource generator!')
        return None
    for path, content in protoerror.finding.iter_findings(source):  # pylint:disable=W0612,W0621
        if not content:
            # no finding in `path`
            continue
        first = content[0].number
        return first
    return None


TEST_DOCUMENT = 'home_home025'
TEST_DOCUMENT_B = 'home_home018'
TODO_DOCUMENT = 'docu_docu007'
TEST_FINDING = first_finding(TEST_DOCUMENT)
INVALID_DOCUMENT = 'rrrrrrrrrrrrrrrr'
INVALID_SECOND = 'SSSSSSSSSSSSSSSS'

MINIMAL = hoverpower.DOCU007_PDF
assert os.path.exists(MINIMAL), MINIMAL

EXAMPLE_READY = hoverpower.generated(folder='ready')

EXAMPLE_TODO = hoverpower.generated(folder='todo')

EXAMPLE_ROOT = os.path.join(EXAMPLE_READY, TEST_DOCUMENT)
EXAMPLE_RESULT = os.path.join(EXAMPLE_ROOT, 'result')

TEST_USER = 'eewuesteewuestee'
TEST_PASSWORD = 'EEWUESTEEWUESTEE'  # nosec
TEST_EMAIL = 'dertestbaer@helm.com'

generated = pytest.mark.skipif(
    not utilo.exists(EXAMPLE_RESULT),
    reason='generate data',
)


@contextlib.contextmanager
def test_user(mp):
    with mp.context() as context:

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
    result = utilotest.apiupload(
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
    result = utilotest.apicall(
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
