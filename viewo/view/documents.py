# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login
import link
import utila

import viewo.api.documents.present

documents_ = flask.Blueprint('documents', __name__)  # pylint:disable=C0103


@documents_.route('/documents', methods=['GET'])
def view_documents():
    done = utila.str2bool(flask.request.args.get('done', False))
    public = utila.str2bool(flask.request.args.get('public', False))
    owner = userid(public=public)
    documents = viewo.api.documents.present.load_documents(
        owner,
        done=done,
    )
    return flask.render_template('documents/index.html', documents=documents)


@documents_.route('/document_compare', methods=['GET'])
def document_compare():
    return flask.render_template('documents/compare.html')


def userid(public: bool = True):
    """Select filter policy by loggend in user. Decide to show private,
    public or both data."""
    user = flask_login.current_user.get_id()
    user = {link.PUBLIC_OWNER} if user is None else user
    if not public:
        return user
    if user:
        # add public documents to user
        user = {link.PUBLIC_OWNER, user}
    return user
