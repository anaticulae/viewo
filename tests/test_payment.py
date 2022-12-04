# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import pytest

import tests
import viewo.config
import viewo.view.payment

BADGETEXT = '>Vollzugriff erhalten</button>'


@pytest.mark.parametrize('payment', (True, False))
def test_payment_badge(user_client, payment, mp):
    """User is logged in and no payment is done."""
    with setpayment(payment, mp):
        home = tests.content(user_client, '/')
    assert (BADGETEXT in home) == payment


def test_payment_nobadge_after_payment(user_client, mp):
    """Login and Pay. Badge disappear after paying."""
    with setpayment(True, mp):
        home = tests.content(user_client, '/')
        assert BADGETEXT in home
        # pay
        payed = tests.post(user_client, '/payment', data=dict(choice=2))
        assert BADGETEXT not in payed
        # home without badge
        home = tests.content(user_client, '/')
        assert BADGETEXT not in home


def test_payment_invalid_choice(user_client, mp):
    with setpayment(True, mp):
        failure = tests.post(user_client, '/payment', data=dict(choice='ABC'))
    # flashed error message
    assert viewo.view.payment.INVALID_MESSAGE in failure


def test_payment_post_nochoice(user_client, mp):
    with setpayment(True, mp):
        failure = tests.post(user_client, '/payment', data={})
    assert viewo.view.payment.NO_PRODUCT_CHOICE in failure


@contextlib.contextmanager
def setpayment(payment, mp):
    with mp.context() as context:
        context.setattr(viewo.config, 'PAYMENT', payment)
        yield
