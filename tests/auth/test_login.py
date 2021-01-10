# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests


def test_auth_login_open(test_client):
    result = tests.content(test_client, '/login')
    assert 'Benutzer:' in result
    assert 'Passwort:' in result


def test_auth_login_click(test_client):
    # run login
    result = tests.post(
        test_client,
        '/login',
        dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
    )
    assert 'Login erfolgreich' in result
    # run login again, forward to document list
    result = tests.post(
        test_client,
        '/login',
        dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
    )
    assert '<h2>Dokumente</h2>' in result


def test_auth_login_invalid_password(test_client):
    result = tests.post(
        test_client,
        '/login',
        dict(user=tests.TEST_USER, password='wrong password'),  # nosec
    )
    assert 'Benutzerdaten fehlerhaft' in result
    # login view visible
    assert '<h1>Login</h1>' in result


def test_auth_logout_click(user_client):
    """Use fixture with logged in user. Click logout and login again."""
    # logout
    result = tests.content(user_client, '/logout')
    assert 'Logout erfolgreich' in result

    # login again
    result = tests.post(
        user_client,
        '/login',
        dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
    )
    assert 'Login erfolgreich' in result


def test_auth_for_required_page(test_client):
    """Ensure that logging in for private page forwards correctly."""
    result = tests.post(
        test_client,
        '/login?next=account',
        dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
    )
    assert '<h1>Account Übersicht</h1>' in result
