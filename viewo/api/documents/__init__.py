# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import utila

api_documents = flask.Blueprint('api_documents', __name__)  # pylint:disable=C0103

__all__ = ['api_documents', 'delete', 'present']

DOCUMENTID_LENGTH = 16
DOCUMENTID = f'<string(length={DOCUMENTID_LENGTH}):documentid>'
DOCUMENTID_B = f'<string(length={DOCUMENTID_LENGTH}):partnerid>'
if utila.testing():
    # allow invalid document length
    DOCUMENTID = '<string:documentid>'
    DOCUMENTID_B = '<string:partnerid>'
