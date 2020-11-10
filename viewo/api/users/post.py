# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import viewo.api.users.utils
import viewo.api.users.utils.user


def create_user(userid: str = None, password: str = None) -> tuple:
    """Private service to generate new user.

    Args:
        userid(str): unique userid to indentify user - if None, random
                     userid is created
        password(str): clear text password - if None, random password is
                     created
    Returns:
        userid, password

    TODO: THINK ABOUT CONVERTING TO HTTP/PUBLIC SERVICE.
    """
    if not password:
        password = viewo.api.users.utils.password.generate()
    created = viewo.api.users.utils.user.create_user(
        password=password,
        userid=userid,
    )
    userid = created.userid
    return userid, password
