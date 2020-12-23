# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import functools

import flask
import flask_login
import link
import utila

import viewo.api.users.utils.user
import viewo.api_.findings.update


def success(message: str = 'completed', **args):
    result = flask.jsonify({
        'message': message,
        **args,
    })
    return result, 200


def notfound(message: str):
    result = flask.jsonify({
        'error': 'not found',
        'message': message,
    })
    return result, 404


def bad(message: str):
    result = flask.jsonify({
        'error': 'bad request',
        'message': message,
    })
    return result, 400


def internal(message: str):
    result = flask.jsonify({
        'error': 'internal',
        'message': message,
    })
    return result, 500


def valid_document(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        documentid = kwargs['documentid']
        documentpath = link.document(documentid)
        if documentpath is None:
            return notfound(f'could not locate `{documentid}`')
        if not accessable(documentid):
            return notfound('not accessable')
        return function(*args, **kwargs)

    return decorated_function


def accessable(documentid: str):
    userid = flask_login.current_user.get_id()
    try:
        # TODO: INVESTIGATE THIS HACK
        job = link.load_jobinfo(documentid, done=False)
    except FileNotFoundError:
        return True
    if job.owner == link.PUBLIC_OWNER:
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
        documentpath = link.document(documentid)
        if documentpath is None:
            return notfound(f'could not locate `{documentid}`')
        return function(*args, **kwargs)

    return decorated_function


def valid_finding(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        documentid = kwargs['documentid']
        findingid = kwargs['findingid']
        finding = viewo.api_.findings.loader.load_finding(documentid, findingid)
        if not finding:
            return notfound(f'could not locate: {findingid}')
        return function(*args, **kwargs)

    return decorated_function


def valid_user(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        userid = kwargs['userid']
        user = viewo.api.users.utils.user.user_fromid(userid)
        if not user:
            return notfound(f'could not locate: {userid}')
        return function(*args, **kwargs)

    return decorated_function


def valid_pages(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER PAYMENT CHECK
        documentid = kwargs['documentid']
        # with contextlib.suppress(KeyError):
        pages = flask.request.args.get('pages', None)
        if pages is None:
            pages = flask.request.args.get('pages', None)
        else:
            pagecount = viewo.api.pageviews.utils.pagecount(documentid)
            selected = utila.parse_pages(pages, pagecount=pagecount)
            if selected is None:
                return bad(f'invalid page count: {pages}')
            if len(selected) > pagecount:
                return bad(f'invalid page count: {len(selected)}>{pagecount}')
        return function(*args, **kwargs)

    return decorated_function


def login_required_api(func):

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            return notfound('login required')
        return func(*args, **kwargs)

    return decorated_view
