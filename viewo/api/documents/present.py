# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json
import os

import flask
import flask_login
import qvlink
import utilo
import viewo_api

import viewo.api
import viewo.api.documents
import viewo.api.documents.utils
import viewo.path
import viewo.result.loader.log


@viewo.api.documents.api_documents.route('/documents', methods=['GET'])
def documents():
    state = docstate()
    owner = curowner()
    collected = load_documents(owner=owner, state=state)
    dumped = json.dumps({
        'documents': collected,
    })
    return dumped


def docstate() -> qvlink.State:
    state = flask.request.args.get('state', None)
    if state is None:
        return state
    try:
        result = qvlink.State.fromstr(state)
    except ValueError:
        result = qvlink.State.DONE
    return result


def curowner() -> set:
    public = utilo.str2bool(flask.request.args.get('public', False))
    result = userid(public=public)
    return result


def load_documents(owner, state: qvlink.State = None) -> list:
    common = viewo.path.common()
    result = qvlink.load_documents(
        common=common,
        owner=owner,
        state=state,
    )
    return result


def userid(public: bool = True) -> set:
    """Select filter policy by loggend in user.

    Decide to show private, public or both data.
    """
    # TODO: ADD UNIT TEST
    user = flask_login.current_user.get_id()
    user = {qvlink.PUBLIC_OWNER} if user is None else {user}
    if public:
        # user = user | {qvlink.PUBLIC_OWNER}
        user = {qvlink.PUBLIC_OWNER}
    return user


@viewo.api.documents.api_documents.route(
    f'/documents/{viewo.api.documents.DOCUMENTID}',
    methods=['GET'],
)
@viewo.api.valid_document
def document_get(documentid: str):
    """Receive document information selected by documentid. If document
    does not exists, 404 Error will be raised."""
    loaded = qvlink.load_jobinfo_raw(documentid, done=None)
    if not loaded:
        return viewo_api.notfound(f'could not locate `{documentid}')
    dumped = json.dumps({
        'document': loaded,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    f'/documents/{viewo.api.documents.DOCUMENTID}/pdf',
    methods=['GET'],
)
@viewo.api.valid_document
def pdf_get(documentid: str) -> bytes:
    todo = qvlink.todo(documentid)
    pdf = os.path.join(todo, documentid)
    if not os.path.exists(pdf):
        return 'NO DOCUMENT', 404
    loaded = utilo.file_read_binary(pdf)
    return loaded


@viewo.api.documents.api_documents.route(
    f'/documents/{viewo.api.documents.DOCUMENTID}/footnotes',
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
    f'/documents/{viewo.api.documents.DOCUMENTID}/style',
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
    f'/documents/{viewo.api.documents.DOCUMENTID}/captions',
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
    f'/documents/{viewo.api.documents.DOCUMENTID}/bibliography',
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
    f'/documents/{viewo.api.documents.DOCUMENTID}/properties',
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
    f'/documents/{viewo.api.documents.DOCUMENTID}/links',
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
    f'/documents/{viewo.api.documents.DOCUMENTID}/pagenumbers',
    methods=['GET'],
)
@viewo.api.valid_document
def pagenumbers_get(documentid: str):
    simple = viewo.api.documents.utils.pagenumbers(documentid)
    dumped = json.dumps({
        'pagenumbers': simple,
    })
    return dumped


@viewo.api.no_production
@viewo.api.documents.api_documents.route(
    f'/documents/{viewo.api.documents.DOCUMENTID}/log',
    methods=['GET'],
)
@viewo.api.valid_document
def log_get(documentid: str):
    content = viewo.result.loader.log.load_fromdocumentid(documentid)
    return content
