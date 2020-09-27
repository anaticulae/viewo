# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json
import os

import link
import link.job

import viewo.api
import viewo.api.documents
import viewo.api.documents.utils


@viewo.api.documents.api_documents.route('/documents', methods=['GET'])
def documents():
    collected = viewo.api.documents.utils.all_documents()
    dumped = json.dumps({
        'documents': collected,
    })
    return dumped


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>',
    methods=['GET'],
)
@viewo.api.valid_document
def document_get(documentid: str):
    """Recieve document information selected by documentid. If document
    does not exists, 404 Error will be raised."""
    source = os.path.join(link.document(documentid), link.JOB_FILE_NAME)  # pylint:disable=E1101
    if not os.path.exists(source):
        return viewo.api.notfound(f'could not locate `{documentid}')
    # TODO: REPLACE WITH JSON METHOD
    loaded = viewo.api.documents.utils.job_toraw(link.load_job(source))
    dumped = json.dumps({
        'document': loaded,
    })
    return dumped


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
