# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import viewo_api

import viewo.api
import viewo.api.documents


@viewo.api.documents.api_documents.route(
    f'/documents/{viewo.api.documents.DOCUMENTID}',
    methods=['DELETE'],
)
@viewo.api.valid_document
def document_delete(documentid) -> str:
    current = link.current(documentid)
    if current == link.ProcessState.UNDEFINED:
        return viewo_api.internal('unexpected state')
    if current == link.ProcessState.DELETED:
        return viewo_api.bad('resource was already deleted')
    link.delete(documentid)
    return viewo_api.success(f'deleted: {documentid}')
