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
import link
import utila

import viewo.api.findings.utils
import viewo.api.users.utils


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
        return function(*args, **kwargs)

    return decorated_function


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
        finding = viewo.api.findings.utils.load_finding(documentid, findingid)
        if not finding:
            return notfound(f'could not locate: {findingid}')
        return function(*args, **kwargs)

    return decorated_function


def valid_user(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER RIGHTS CHECK
        userid = kwargs['userid']
        user = viewo.api.users.utils.user_fromid(userid)
        if not user:
            return notfound(f'could not locate: {userid}')
        return function(*args, **kwargs)

    return decorated_function


def valid_pages(function):

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        # TODO: ADD USER PAYMENT CHECK
        documentid = kwargs['documentid']
        with contextlib.suppress(KeyError):
            pages = flask.request.args['range']
            pagecount = viewo.api.pages.utils.pagecount(documentid)
            selected = utila.parse_pages(pages, pagecount=pagecount)
            if selected is None:
                return bad(f'invalid page count: {pages}')
            if len(selected) > pagecount:
                return bad(f'invalid page count: {len(selected)}')
        return function(*args, **kwargs)

    return decorated_function
