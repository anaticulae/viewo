# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import utilo

api_documents = flask.Blueprint('api_documents', __name__)  # pylint:disable=C0103

__all__ = ['api_documents', 'delete', 'present']

# pylint: disable=invalid-name
DOCUMENTID_LENGTH = 16  # TODO: USE CONFIGO
DOCUMENTID = f'<string(length={DOCUMENTID_LENGTH}):documentid>'
DOCUMENTID_B = f'<string(length={DOCUMENTID_LENGTH}):partnerid>'
if utilo.testing():
    # allow invalid document length
    DOCUMENTID = '<string:documentid>'
    DOCUMENTID_B = '<string:partnerid>'
