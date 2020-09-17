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
    '/documents/<string:documentid>',
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
