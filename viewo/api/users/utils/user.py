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
import viewo.api.users.utils.password
import viewo.config

USER_LENGTH = 16  # TODO: HOLY VALUE


def users():
    common_user = viewo.api.users.data.load_users(viewo.config.USERS)
    raw = [viewo.api.users.data.user_raw(item) for item in common_user]
    return raw


def user_fromid(userid: str) -> 'viewo.api.users.data.User':
    if userid == 'test':
        fake = viewo.api.users.data.User(
            userid='test',
            password=viewo.api.users.utils.password.hashed('testtest'),
            email='test@testo.te',
        )
        return fake
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


def create_user(password: str):
    # validate password
    password = viewo.api.users.utils.password.hashed(password)
    # generate new random user name
    random = utila.tmpname(USER_LENGTH)
    while os.path.exists(user_path(random)):
        random = utila.tmpname(USER_LENGTH)
    new = viewo.api.users.data.User(userid=random, password=password)
    # write to user database
    user_update(new)
    return new


def user_document_append(userid: str, documentid: str):
    user = user_fromid(userid)
    user.append_document(documentid)
    user_update(user)


def valid_username(name) -> False:
    """\
    >>> valid_username('not a valid user')
    False
    >>> valid_username('012ABxxF012ABxxF')
    True
    >>> valid_username(' 12  xxx')
    False
    """
    if not len(name) == USER_LENGTH:
        return False
    return all(item.isalnum() for item in name)
