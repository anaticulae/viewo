# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link

import viewo.api
import viewo.api.documents


@viewo.api.documents.api_documents.route(
    '/documents/<string(length=16):documentid>',
    methods=['DELETE'],
)
@viewo.api.valid_document
def document_delete(documentid) -> str:
    current = link.current(documentid)
    if current == link.ProcessState.UNDEFINED:
        return viewo.api.internal('unexpected state')
    if current == link.ProcessState.DELETED:
        return viewo.api.bad('resource was already deleted')
    link.delete(documentid)
    return viewo.api.success(f'deleted: {documentid}')
