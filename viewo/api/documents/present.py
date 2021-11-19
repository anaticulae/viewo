# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json
import os

import flask
import flask_login
import link
import utila
import viewo_api

import viewo.api
import viewo.api.documents
import viewo.api.documents.utils
import viewo.path


@viewo.api.documents.api_documents.route('/documents', methods=['GET'])
def documents():
    done = utila.str2bool(flask.request.args.get('done', False))
    public = utila.str2bool(flask.request.args.get('public', False))
    owner = userid(public=public)
    collected = load_documents(owner, done=done)
    dumped = json.dumps({
        'documents': collected,
    })
    return dumped


def load_documents(owner, done: bool = False):
    common = viewo.path.common()
    todo, ready = link.collect_jobs(common, skip_removed=True, owner=owner)
    if done:
        # do not load jobs which are not done
        todo.clear()
    dones = {item.name for item in ready}
    result = [link.load_jobinfo_raw(item.name, done=None) for item in ready]
    for item in result:
        item['done'] = True
    for item in todo:
        if item.name in dones:
            continue
        current = link.load_jobinfo_raw(item.name, done=None)
        result.append(current)
    result = sorted(
        result,
        key=lambda item: link.sortable_date(item['date']),
        reverse=True,
    )
    return result


def userid(public: bool = True):
    """Select filter policy by loggend in user. Decide to show private,
    public or both data."""
    # TODO: REMOVE DUPLICATION LATER
    # TODO: ADD UNIT TEST
    user = flask_login.current_user.get_id()
    user = {link.PUBLIC_OWNER} if user is None else {user}
    if public:
        # user = user | {link.PUBLIC_OWNER}
        user = {link.PUBLIC_OWNER}
    return user


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>',
    methods=['GET'],
)
@viewo.api.valid_document
def document_get(documentid: str):
    """Receive document information selected by documentid. If document
    does not exists, 404 Error will be raised."""
    loaded = link.load_jobinfo_raw(documentid, done=None)
    if not loaded:
        return viewo_api.notfound(f'could not locate `{documentid}')
    dumped = json.dumps({
        'document': loaded,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/pdf',
    methods=['GET'],
)
@viewo.api.valid_document
def pdf_get(documentid: str) -> bytes:
    todo = link.todo(documentid)
    pdf = os.path.join(todo, documentid)
    if not os.path.exists(pdf):
        return 'NO DOCUMENT', 404
    loaded = utila.file_read_binary(pdf)
    return loaded


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/footnotes',
    methods=['GET'],
)
@viewo.api.valid_document
def footnotes_get(documentid: str):
    simple = viewo.api.documents.utils.footnotes(documentid)
    dumped = json.dumps({
        'footnotes': simple,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/style',
    methods=['GET'],
)
@viewo.api.valid_document
def docstyle_get(documentid: str):
    simple = viewo.api.documents.utils.style(documentid)
    dumped = json.dumps({
        'style': simple,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/captions',
    methods=['GET'],
)
@viewo.api.valid_document
def captions_get(documentid: str):
    simple = viewo.api.documents.utils.captions(documentid)
    dumped = json.dumps({
        'captions': simple,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/bibliography',
    methods=['GET'],
)
@viewo.api.valid_document
def bibliography_get(documentid: str):
    simple = viewo.api.documents.utils.bibliography(documentid)
    dumped = json.dumps({
        'bibliography': simple,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/properties',
    methods=['GET'],
)
@viewo.api.valid_document
def properties_get(documentid: str):
    simple = viewo.api.documents.utils.properties(documentid)
    dumped = json.dumps({
        'properties': simple,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/links',
    methods=['GET'],
)
@viewo.api.valid_document
def links_get(documentid: str):
    simple = viewo.api.documents.utils.links(documentid)
    dumped = json.dumps({
        'links': simple,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>/pagenumbers',
    methods=['GET'],
)
@viewo.api.valid_document
def pagenumbers_get(documentid: str):
    simple = viewo.api.documents.utils.pagenumbers(documentid)
    dumped = json.dumps({
        'pagenumbers': simple,
    })
    return dumped
