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
    todo, ready = link.collect_jobs(common)

    docs = todo + ready
    docs = unify(docs)
    # sort by date
    docs = sorted(
        docs,
        key=lambda item: link.sortable_date(item.date),
        reverse=True,
    )
    return flask.render_template('documents/index.html', documents=docs)


def unify(items):
    done_index = {item.index for item in done(items)}

    result = done(items)
    for item in items:
        if item.index in done_index:
            # job is already done
            continue
        result.append(item)
    return result


def done(items):
    return [item for item in items if item.result]
