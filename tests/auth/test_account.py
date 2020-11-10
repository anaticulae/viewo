# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests
import tests.api


def test_account_show(user_client):
    result = tests.content(user_client, '/account')
    assert 'Account' in result


def test_account_change_password(user_client):
    tests.api.password_change(user_client, 'helmistoll', 'helmistoll')
    tests.api.logout(user_client)
    tests.api.login(user_client, tests.TEST_USER, password='helmistoll')
