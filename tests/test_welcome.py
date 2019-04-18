# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from tests import BASE_TEMPLATE
from tests import result


def test_index(client):
    response = client.get('/')
    content = result(response)
    assert content
    assert len(content) > len(BASE_TEMPLATE), content


def test_error(client):
    response = client.get('thispagedoesnotexists_ihopeso')
    content = result(response)
    assert content
    assert 'Fehler' in content
