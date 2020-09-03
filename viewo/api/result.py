# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import link
import protocol
import utila

import viewo.result.update

result_ = flask.Blueprint('result', __name__)  # pylint:disable=C0103


@result_.route('/result', defaults={'document': None})
@result_.route('/result/<string:document>')
def view_result(document: str = None):
    if not document:
        return flask.redirect(flask.url_for('documents.view_documents'))

    invalid_document = not os.path.exists(link.ready(document))
    if invalid_document:
        return flask.redirect('result/failure')

    rendered = flask.render_template(
        'result/index.html',
        process=document,
        waiting=False,
    )
    return rendered


@result_.route('/result/<string:document>/<string:image>')
def view_images(document: str = None, image: str = None):
    document = str(document)
    source = link.ready(document)
    invalid_document = not os.path.exists(source)
    if invalid_document:
        utila.error(f'could not load document: {source}')
        return flask.redirect('result/failure')
    image = os.path.join(source, 'result/view/', image)
    if not os.path.exists(image):
        utila.error(f'could not load image: {image}')
        return flask.redirect('result/failure')
    # contextmanager does not work here
    response = flask.send_file(open(image, mode='rb'), mimetype='image')
    return response


@result_.route(
    '/result/<string:doc>/update/finding/<string:finding>/<int:status>',
    methods=['POST'],
)
def update_finding_status(  # pylint:disable=W0613
        doc: str = None,
        finding: int = None,
        status: int = None,
) -> str:
    """Update finding status.

    Args:
        doc(str): document to update
        finding(int): hash value of finding to update, flask support
                      only possitive integers, therefore we have to use
                      string and convert them here.
        status(int): new status
    Returns:
        `done` if update was successful else `failed`
    """
    source = link.ready(doc)
    invalid_document = not os.path.exists(source)
    if invalid_document:
        utila.error(f'could not load document: {source}')
        return 'failed'
    try:
        finding = int(finding)
    except ValueError:
        return 'failed'

    status = viewo.result.update.problem_fromint(status)
    before = protocol.finding_status(source, finding)
    if not protocol.finding_status_update(source, finding, status):
        utila.error(f'could not update: {finding} status: {status}')
    else:
        viewo.result.update.update_bookkeeping(source, status, before)
    return 'done'


@result_.route('/result/failure')
def failure():
    return flask.render_template('result/failure.html')
