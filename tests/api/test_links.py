# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

import tests


def test_regression_api_links(findingclient):
    """Test that non existing links produces empty list and not None."""
    result = utilotest.apicall(
        findingclient,
        f'/documents/{tests.TEST_DOCUMENT}/links',
    )
    # empty links list
    assert result['links']['resource'] == []
