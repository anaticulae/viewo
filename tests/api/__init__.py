# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests


def login(client, userid=tests.TEST_USER, password=tests.TEST_PASSWORD):
    result = tests.post(
        client,
        '/login',
        dict(user=userid, password=password),
    )
    print(result)
    assert 'Login erfolgreich' in result


def logout(client):
    tests.content(client, '/logout')
