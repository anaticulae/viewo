# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import functools

import flask
import flask_login
import qvlink
import utilo
import viewo_api
import viewo_api.user.data

import viewo.api_.findings.data
import viewo.api_.findings.update
import viewo.config


def valid_document(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        documentid = kwargs['documentid']
        documentpath = qvlink.document(documentid)
        if documentpath is None:
            return viewo_api.notfound(f'could not locate `{documentid}`')
        if not accessable(documentid):
            return viewo_api.notfound('not accessable')
        return function(*args, **kwargs)

    return decorated_function


def accessable(documentid: str):
    userid = flask_login.current_user.get_id()
    try:
        # TODO: INVESTIGATE THIS HACK
        job = qvlink.load_jobinfo(documentid, done=False)
    except FileNotFoundError:
        return True
    if job.owner == qvlink.PUBLIC_OWNER:
        return True
    if userid is None:
        return False
    return userid == job.owner


# TODO: IMPROVE DECORATOR KNOWLEDGE
def valid_partner(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        documentid = kwargs['partnerid']
        documentpath = qvlink.document(documentid)
        if documentpath is None:
            return viewo_api.notfound(f'could not locate `{documentid}`')
        return function(*args, **kwargs)

    return decorated_function


def valid_finding(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        documentid = kwargs['documentid']
        findingid = kwargs['findingid']
        try:
            viewo.api_.findings.data.frontend(documentid)[findingid]
        except KeyError:
            return viewo_api.notfound(f'could not locate finding: {findingid}')
        return function(*args, **kwargs)

    return decorated_function


def valid_user(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        userid = kwargs['userid']
        user = viewo_api.user.data.user_fromid(userid)
        if not user:
            return viewo_api.notfound(f'could not locate: {userid}')
        return function(*args, **kwargs)

    return decorated_function


def valid_pages(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER PAYMENT CHECK
        pages = flask.request.args.get('pages', None)
        if pages is None:
            return function(*args, **kwargs)
        # verify selected pages
        documentid = kwargs['documentid']
        pagecount = viewo.api.pageviews.utils.pagecount(documentid)
        selected = utilo.parse_pages(pages, pagecount=pagecount)
        if selected is None:
            return viewo_api.bad(f'invalid page count: {pages}')
        if len(selected) > pagecount:
            start = min(selected)
            if start >= pagecount:
                return viewo_api.bad(
                    f'invalid page count: {len(selected)}>{pagecount}')
        return function(*args, **kwargs)

    return decorated_function


def login_required_api(func):

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            return viewo_api.notfound('login required')
        return func(*args, **kwargs)

    return decorated_view


def no_production(func):

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if viewo.config.PRODUCTION:
            return viewo_api.bad('invalid access')
        return func(*args, **kwargs)

    return decorated_view
