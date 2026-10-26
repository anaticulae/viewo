# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

from tests.selenium.utils import text_inclass

FORM = 'form-group'


@utilotest.nightly
@utilotest.displayed
def test_upload_switch(driver, webview):
    """Ensure that changing user source works. First selenium test ;)."""
    driver.get(webview)
    driver.find_elements_by_name('url')
    assert not text_inclass('Webadresse oder Cloudspeicher:', FORM, driver)
    driver.find_element_by_partial_link_text('URL').click()
    assert text_inclass('Webadresse oder Cloudspeicher:', FORM, driver)

    driver.find_element_by_partial_link_text('Lokale Datei').click()
    assert text_inclass('Wählen Sie Ihr PDF Dokument aus:', FORM, driver)
