# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import viewo.api.users.data
import viewo.config


def users():
    common_user = viewo.api.users.data.load_users(viewo.config.USERS)
    raw = [viewo.api.users.data.user_raw(item) for item in common_user]
    return raw


def user_fromid(userid: str) -> 'viewo.api.users.data.User':
    path = user_path(userid)
    if not os.path.exists(path):
        return None
    loaded = viewo.api.users.data.load_user(path)
    return loaded


def user_path(userid: str) -> str:
    return os.path.join(viewo.config.USERS, f'{userid}.yaml')


def user_update(user: 'viewo.api.users.data.User') -> bool:
    dumped = viewo.api.users.data.dump_user(user)
    path = user_path(user.userid)
    utila.file_replace(path, dumped)
    return True
