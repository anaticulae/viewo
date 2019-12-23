# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests
import viewo.waiting.resultview


def test_resultview_load_resultview():
    loaded = viewo.waiting.resultview.load_resultview(tests.EXAMPLE_RESULT)
    assert loaded, str(loaded)
    # 2 pages
    assert len(loaded) == 2, str(loaded)


def test_resultview_tojson():
    loaded = viewo.waiting.resultview.load_resultview(tests.EXAMPLE_RESULT)
    dumped = viewo.waiting.resultview.tojson(loaded)
    assert 'page' in dumped
    assert 'html' in dumped
    assert 'findings' in dumped
    assert 'title' in dumped
    assert 'location' in dumped
    assert len(dumped) > 450, str(dumped)
