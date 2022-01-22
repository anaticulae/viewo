# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask

import viewo.api.documents.present

documents_ = flask.Blueprint('documents', __name__)  # pylint:disable=C0103


@documents_.route('/documents', methods=['GET'])
def view_documents():
    owner = viewo.api.documents.present.curowner()
    documents = viewo.api.documents.present.load_documents(owner)
    return flask.render_template('documents/index.html', documents=documents)


@documents_.route('/document_compare', methods=['GET'])
def document_compare():
    return flask.render_template('documents/compare.html')
