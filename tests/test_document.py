# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from viewo.documents import sortable_date


def test_sortable_date():
    # "%02d.%02d.%04d"
    expected = [
        '31.12.2019',
        '31.11.2019',
        '23.04.2019',
        '20.04.2019',
        '01.01.2019',
        '10.02.2018',
        '10.01.2018',
        '01.01.2018',
    ]

    result = [
        '10.01.2018',
        '20.04.2019',
        '10.02.2018',
        '01.01.2018',
        '31.12.2019',
        '23.04.2019',
        '01.01.2019',
        '31.11.2019',
    ]
    result = sorted(result, key=sortable_date, reverse=True)

    assert result == expected
