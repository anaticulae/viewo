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


def create_user():
    """Private service to generate new user.

    TODO: THINK ABOUT CONVERTING TO HTTP/PUBLIC SERVICE.
    """
    password = viewo.api.users.utils.password.generate()
    userid = viewo.api.users.utils.user.create_user(password).userid
    return userid, password
