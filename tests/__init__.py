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

import utila
import werkzeug.datastructures

import viewo.config

TEST_DATA = os.path.join(viewo.config.ROOT, 'tests/data')
assert os.path.exists(TEST_DATA), TEST_DATA

BASE_TEMPLATE = utila.file_read(os.path.join(viewo.config.TEMPLATES, 'base.html')) # yapf:disable

MINIMAL = os.path.join(TEST_DATA, 'minimal.pdf')
assert os.path.exists(MINIMAL), MINIMAL

EXAMPLE_READY = os.path.join(TEST_DATA, 'ready')
assert os.path.exists(EXAMPLE_READY), EXAMPLE_READY

EXAMPLE_TODO = os.path.join(TEST_DATA, 'todo')
assert os.path.exists(EXAMPLE_TODO), EXAMPLE_TODO

EXAMPLE_RESULT = os.path.join(EXAMPLE_READY, '1508790764/result')
assert os.path.exists(EXAMPLE_RESULT), EXAMPLE_RESULT


def decode(response) -> dict:
    """Read binary data from response and convert them to str"""
    result = response.data.decode('utf8')
    with contextlib.suppress(json.decoder.JSONDecodeError):
        # json format
        return json.loads(result)
    # html format
    return result


def content(client, request: str):
    response = client.get(request)
    assert response.status_code == http.HTTPStatus.OK
    return decode(response)


def apicall(
        client,
        request: str,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    cmd = prefix + request
    response = client.get(cmd)
    assert response.status_code == expected, str(response.status_code)
    return decode(response)


def apidelete(
        client,
        request: str,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    cmd = prefix + request
    response = client.delete(cmd)
    assert response.status_code == expected, str(response.status_code)
    return decode(response)


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
    cmd = prefix + page
    fields = werkzeug.datastructures.MultiDict([(field, open(path, 'rb'))])
    response = client.post(cmd, data=fields, follow_redirects=True)
    assert response.status_code == expected, str(response.status_code)
    return decode(response)


def upload(client, file=MINIMAL):
    result = apiupload(
        client,
        '/documents',
        'file',
        file,
    )
    return result


def apipost(
        client,
        page: str,
        data: dict,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    cmd = prefix + page
    result = client.post(cmd, data=data, follow_redirects=True)
    assert result.status_code == expected, str(result)
    return decode(result)


def apiput(
        client,
        page: str,
        data: dict,
        prefix=viewo.config.API_PREFIX,
        expected=http.HTTPStatus.OK,
):
    cmd = prefix + page
    result = client.put(cmd, data=data, follow_redirects=True)
    assert result.status_code == expected, str(result)
    return decode(result)


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
