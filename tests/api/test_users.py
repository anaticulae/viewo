# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import tests


def test_api_users(client):
    result = tests.apicall(client, '/users')
    assert result['users']
    assert result['users']['uri']


def test_api_user_get(user_client):
    result = tests.apicall(user_client, f'/users/{tests.TEST_USER}')
    assert result['user']['email'] == tests.TEST_EMAIL
    assert result['user']['user'] == tests.TEST_USER
    assert result['uri']


def test_api_user_not_logged_in(test_client):
    result = tests.apicall(
        test_client,
        f'/users/{tests.TEST_USER}',
        expected=http.HTTPStatus.NOT_FOUND,
    )
    assert result['message'] == 'login required'
