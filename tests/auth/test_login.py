# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests


def test_auth_login_open(client):
    result = tests.content(client, '/login')
    assert 'Benutzer:' in result
    assert 'Passwort:' in result


def test_auth_login_click(client, monkeypatch):
    # run login
    with tests.test_user(monkeypatch):
        result = tests.post(
            client,
            '/login',
            dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
        )
    assert 'Login erfolgreich' in result
    # run login again, forward to document list
    with tests.test_user(monkeypatch):
        result = tests.post(
            client,
            '/login',
            dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
        )
    '<h2>Dokumente</h2>' in result


def test_auth_login_invalid_password(client, monkeypatch):
    with tests.test_user(monkeypatch):
        result = tests.post(
            client,
            '/login',
            dict(user=tests.TEST_USER, password='wrong password'),
        )
    assert 'Benutzerdaten fehlerhaft' in result
    # login view visible
    assert '<h1>Login</h1>' in result


def test_auth_logout_click(user_client, monkeypatch):
    """Use fixture with logged in user. Click logout and login again."""
    # logout
    result = tests.content(user_client, '/logout')
    assert 'Logout erfolgreich' in result

    # login again
    with tests.test_user(monkeypatch):
        result = tests.post(
            user_client,
            '/login',
            dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
        )
    assert 'Login erfolgreich' in result
