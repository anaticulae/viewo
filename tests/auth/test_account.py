# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import pytest

import tests
import tests.api
import viewo.api.users.update


def test_account_show(user_client):
    result = tests.content(user_client, '/account')
    assert 'Account' in result


def test_account_change_password(user_client):
    tests.api.password_change(user_client, 'helmisto', 'helmisto')
    tests.api.logout(user_client)
    tests.api.login(user_client, tests.TEST_USER, password='helmisto')  # nosec


@pytest.mark.parametrize(
    'password_new, password_new_repeat, expected',
    [
        pytest.param(
            'helm',
            'helm',
            viewo.api.users.update.PASSWORD_NEW_TOO_SHORT,
            id='too_short',
        ),
        pytest.param(
            'a' * 70,
            'a' * 70,
            viewo.api.users.update.PASSWORD_NEW_TOO_LONG,
            id='too_long',
        ),
        pytest.param(
            'not matched',
            'not matched_',
            viewo.api.users.update.PASSWORD_DOES_NOT_MATCH,
            id='not matched',
        ),
    ],
)
def test_account_change_password_error(
        user_client,
        password_new,
        password_new_repeat,
        expected,
):
    tests.api.password_change(
        user_client,
        password_new,
        password_new_repeat,
        expected=(expected, http.HTTPStatus.BAD_REQUEST),
    )


def test_account_change_password_invalid_password(user_client):
    tests.api.password_change(  # nosec
        user_client,
        'validpassword',
        'validpassword',
        password='wrongpassword',
        expected=(
            viewo.api.users.update.PASSWORD_WRONG,
            http.HTTPStatus.BAD_REQUEST,
        ),
    )
