# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests


def test_index(client):
    """Open welcome page and check that template is rendered correctly"""
    response = client.get('/')
    content = tests.decode(response)
    assert content
    assert len(content) > len(tests.BASE_TEMPLATE), content


def test_error(client):
    """Test welcome error handler

    TODO: Redirect to global error handler?
    """
    response = client.get('thispagedoesnotexists_ihopeso')
    content = tests.decode(response)
    assert content
    assert 'Fehler' in content


def test_404_handler(client):
    """Test global error handler"""
    response = client.get('/abc/existiert_nicht')
    content = tests.decode(response)
    assert content
    assert 'Fehler' in content
