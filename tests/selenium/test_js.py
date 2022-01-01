# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utilatest

import viewo


@utilatest.nightly
@utilatest.displayed
def test_javascript(driver):
    path = f'file:///{viewo.ROOT}/tests/js/index.html'
    driver.get(path)
    text = driver.find_element_by_id('qunit').text
    utila.error(text)
    assert 'tests completed' in text
    assert '0 failed.' in text
