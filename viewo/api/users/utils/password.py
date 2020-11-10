# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import viewo.config

# TODO: HOLY SECURE VALUE # CONFIGO!
PASSWORD_SALT = 'THISISSALT'
PASSWORD_RANDOM_LENGTH = 16


class PasswordError(ValueError):
    pass


class PasswordTooShort(PasswordError):
    pass


class PasswordTooLong(PasswordError):
    pass


def valid(password: str) -> bool:
    """\
    >>> valid('short')
    Traceback (most recent call last):
        ...
    viewo.api.users.utils.password.PasswordTooShort

    >>> valid('VeryLongPassword1337')
    True
    """
    if password is None:
        return False
    password = str(password)
    if len(password) < viewo.config.PASSWORD_MIN_LENGTH:
        raise PasswordTooShort
    if len(password) > viewo.config.PASSWORD_MAX_LENGTH:
        raise PasswordTooLong
    return True


def generate() -> str:
    random = utila.tmpname(PASSWORD_RANDOM_LENGTH)
    return random


def hashed(password: str) -> str:
    valid(password)
    password = utila.secure_hash(password, salt=PASSWORD_SALT)  # pylint:disable=E1101
    return password
