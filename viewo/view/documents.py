# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_login
import link
import utila

import viewo.path

documents_ = flask.Blueprint('documents', __name__)  # pylint:disable=C0103


@documents_.route('/documents', methods=['GET'])
def view_documents():
    public = utila.str2bool(flask.request.args.get('public', False))
    owner = userid(public=public)
    documents = load_documents(owner)
    return flask.render_template('documents/index.html', documents=documents)


@documents_.route('/compare_document', methods=['GET'])
def compare_document():
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


def load_documents(owner):
    common = viewo.path.common()
    todo, ready = link.collect_jobs(common, skip_removed=True, owner=owner)
    documents = merge_jobs(todo, ready)
    return documents


def merge_jobs(todo, ready) -> list:
    result = []
    result.extend(ready)
    done = {item.name for item in ready}

    for item in todo:
        if item.name in done:
            continue
        # TODO: REMOVE THIS HACK LATER
        # set to none to have waiting clock in view which symbol the use
        # that document is in progress.
        item.result = None
        result.append(item)

    # sort by date
    result = sorted(
        result,
        key=lambda item: link.sortable_date(item.date),
        reverse=True,
    )
    return result
