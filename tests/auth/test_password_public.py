# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests.api

USER_PASSWORD_INFO = 'Benutzerdaten vergessen haben, ist <u>kein Zugriff auf'


def test_view_public_password_after_ananoym_upload(client):
    """Ensure that user can view password after anonym document upload.

    1. Anonym upload
    2. Check that raw password is show on waiting view
    3. Logout
    4. Login
    5. Ensure that password is !not! shown after loging.
    """
    result = tests.api.upload_minimal(client)
    userid = result['userid']
    password = result['password']
    link = result['link']
    result = tests.content(client, link)

    assert USER_PASSWORD_INFO in result
    assert password in result

    tests.api.logout(client)
    tests.api.login(client, userid=userid, password=password)

    result = tests.content(client, link)
    assert 'Wartebereich' in result
    assert password not in result
    assert USER_PASSWORD_INFO not in result
