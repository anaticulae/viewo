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
from os.path import exists
from os.path import join

import werkzeug.datastructures
from flask import current_app
from utila import file_read

import viewo
import viewo.config
from viewo import create_application
from viewo.config import ROOT
from viewo.config import TEMPLATES

TEST_DATA = join(ROOT, 'tests/data')
assert exists(TEST_DATA), TEST_DATA

BASE_TEMPLATE = file_read(join(TEMPLATES, 'base.html'))

MINIMAL = join(TEST_DATA, 'minimal.pdf')
assert exists(MINIMAL), MINIMAL

EXAMPLE_READY = join(TEST_DATA, 'ready')
assert exists(EXAMPLE_READY), EXAMPLE_READY

EXAMPLE_TODO = join(TEST_DATA, 'todo')
assert exists(EXAMPLE_TODO), EXAMPLE_TODO

EXAMPLE_RESULT = join(EXAMPLE_READY, '1508790764/result')
assert exists(EXAMPLE_RESULT), EXAMPLE_RESULT


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
