# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from tests import BASE_TEMPLATE
from tests import decode


def test_index(client):
    """Open welcome page and check that template is rendered correctly"""
    response = client.get('/')
    content = decode(response)
    assert content
    assert len(content) > len(BASE_TEMPLATE), content


def test_error(client):
    """Test welcome error handler

    TODO: Redirect to global error handler?
    """
    response = client.get('thispagedoesnotexists_ihopeso')
    content = decode(response)
    assert content
    assert 'Fehler' in content


def test_404_handler(client):
    """Test global error handler"""
    response = client.get('/abc/existiert_nicht')
    content = decode(response)
    assert content
    assert 'Fehler' in content
