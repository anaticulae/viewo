# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests

BADGETEXT = '>Vollzugriff erhalten</button>'


def test_payment_bade(user_client):
    """User is logged in and no payment is done."""
    home = tests.content(user_client, '/')
    assert BADGETEXT in home


def test_payment_nobade_after_payment(user_client):
    """Login and Pay. Badge disappear after paying."""
    home = tests.content(user_client, '/')
    assert BADGETEXT in home
    # pay
    payed = tests.post(user_client, '/payment', data=dict(choice=2))
    assert BADGETEXT not in payed
    # home without badge
    home = tests.content(user_client, '/')
    assert BADGETEXT not in home
