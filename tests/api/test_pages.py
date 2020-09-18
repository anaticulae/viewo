# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests

TEST_DOCUMENT = '1508790764'


def test_api_pages_overview(findingclient):
    client = findingclient
    result = tests.apicall(
        client,
        f'/documents/{TEST_DOCUMENT}/pages',
    )
    assert result['pages']
    assert result['pages']['uri']
