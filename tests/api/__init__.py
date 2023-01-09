# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import utilatest

import tests


def login(client, userid=tests.TEST_USER, password=tests.TEST_PASSWORD):
    result = tests.post(
        client,
        '/login',
        dict(user=userid, password=password),
    )
    assert 'Login erfolgreich' in result


def logout(client):
    tests.content(client, '/logout')


def password_change(
        client,
        password_new,
        password_new_repeat,
        password=tests.TEST_PASSWORD,
        expected=('updated', http.HTTPStatus.OK),
):
    data = {
        'password': password,
        'password_new': password_new,
        'password_new_repeat': password_new_repeat,
    }
    result = tests.apiput(
        client,
        f'/users/{tests.TEST_USER}',
        data=data,
        expected=expected[1],
    )
    assert result['message'] == expected[0], str(result)


def email_change(
    client,
    email: str = tests.TEST_EMAIL,
    userid: str = tests.TEST_USER,
    password: str = tests.TEST_PASSWORD,
):
    tests.apiput(
        client,
        f'/users/{userid}',
        data={
            'email': email,
            'password': password,
        },
    )


def upload_minimal(client):
    result = utilatest.apiupload(
        client,
        page='/documents',
        field='file',
        path=tests.MINIMAL,
    )
    return result
