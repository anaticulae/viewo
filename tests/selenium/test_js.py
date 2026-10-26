# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo
import utilotest

import viewo


@utilotest.nightly
@utilotest.displayed
def test_javascript(driver):
    path = f'file:///{viewo.ROOT}/tests/js/index.html'
    driver.get(path)
    text = driver.find_element_by_id('qunit').text
    utilo.error(text)
    assert 'tests completed' in text
    assert '0 failed.' in text
