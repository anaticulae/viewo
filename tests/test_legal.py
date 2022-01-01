# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import tests


def test_impressum(client):
    impressum = tests.content(client, '/impressum')
    assert 'Version' in impressum


@pytest.mark.parametrize(
    'download',
    ['impressum', 'privacy', 'agb'],
)
def test_download_legal(download, client):
    downloaded = tests.content(client, f'download/{download}')
    assert len(downloaded) > 50  # TODO: INCREASE LATER
    # assert 'Version' in downloaded TODO: ENABLE LATER
