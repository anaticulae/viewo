# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilatest

import tests


def test_api_captions_overview(findingclient):
    result = utilatest.apicall(
        findingclient,
        f'/documents/{tests.TEST_DOCUMENT}/captions',
    )
    assert result['captions']
    assert result['captions']['uri']
