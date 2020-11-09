# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import flask
import link

documents_ = flask.Blueprint('documents', __name__)  # pylint:disable=C0103


@documents_.route('/documents', methods=['GET'])
def view_documents():
    common = configo.share()
    # TODO: USE SKIP_REMOVED
    todo, ready = link.collect_jobs(common, skip_removed=True)

    docs = list(ready)
    done = {item.name for item in ready}
    for item in todo:
        if item.name in done:
            continue
        docs.append(item)
    for item in docs:
        # TODO: REMOVE THIS HACK LATER
        if item not in ready:
            # set to none to have waiting clock in view which symbol the
            # use that document is in progress.
            item.result = None
    # sort by date
    docs = sorted(
        docs,
        key=lambda item: link.sortable_date(item.date),
        reverse=True,
    )
    return flask.render_template('documents/index.html', documents=docs)


@documents_.route('/compare_document', methods=['GET'])
def compare_document():
    return flask.render_template('documents/compare.html')
