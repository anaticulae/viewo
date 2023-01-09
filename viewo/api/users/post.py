# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import viewo_api
import viewo_api.user.create
import viewo_api.user.password


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
        password = viewo_api.user.password.password_generate()
    created = viewo_api.user.create.create_user(
        password=password,
        userid=userid,
    )
    userid = created.userid
    return userid, password
