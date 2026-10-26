# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

FORM = 'form-group'

TODO = [  # H2
    ('Dokumente', 'Dokumente'),
    ('Schreibhilfe', 'Suche'),  # Schreibhilfe
    ('Preise', 'Vollzugriff erhalten'),
    ('Login', 'Login'),
    ('Home', 'checkitweg.de'),
    ('Impressum', 'Impressum'),
    ('Kontakt', 'Kontakt'),
    ('Allgemeine Geschäftsbedingungen', 'Allgemeine Geschäftsbedingungen'),
    ('Datenschutzerklärung', 'Datenschutzerklärung'),
]


@utilotest.nightly
@utilotest.displayed
def test_navigation(driver, webview):
    """Ensure that navigation bar works."""
    driver.get(webview)
    for todo, expected in views():
        # open page
        driver.find_element_by_link_text(todo).click()
        # verify headline
        headline = driver.find_element_by_tag_name('h2')
        assert headline.text in expected, headline.text


def views() -> list:
    import viewo.config
    if viewo.config.PAYMENT:
        return TODO
    result = list(TODO)
    del result[2]
    return result
