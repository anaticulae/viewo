# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests


def test_api_properties_overview(findingclient):
    result = tests.apicall(
        findingclient,
        f'/documents/{tests.TEST_DOCUMENT}/properties',
    )
    assert result['properties']
    assert result['properties']['uri']
