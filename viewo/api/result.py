# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io
import os

import flask
import qvlink
import utilo
import utilo.file.securewrapper

import viewo.api.documents

result_ = flask.Blueprint('result', __name__)  # pylint:disable=C0103


@result_.route('/view', defaults={'documentid': None})
@result_.route(f'/view/{viewo.api.documents.DOCUMENTID}')
def view_result(documentid: str = None):
    if not documentid:
        return flask.redirect(flask.url_for('documents.view_documents'))
    invalid_document = not os.path.exists(qvlink.ready(documentid))
    if invalid_document:
        return flask.redirect('view/failure')
    docname = qvlink.job_title(documentid=documentid)
    rendered = flask.render_template(
        'view/index.html',
        process=documentid,
        docname=docname,
        waiting=False,
    )
    return rendered


@result_.route(f'/view/{viewo.api.documents.DOCUMENTID}/<string:image>')
def view_images(documentid: str = None, image: str = None):
    source = qvlink.ready(documentid)
    invalid_document = not os.path.exists(source)
    if invalid_document:
        utilo.error(f'could not load document: {source}')
        return flask.redirect('view/failure')

    image = os.path.join(source, 'result/view/', image)
    if not os.path.exists(image):
        utilo.error(f'could not load image: {image}')
        return flask.redirect('view/failure')

    if qvlink.private(documentid, done=None):
        # Decrypt private image data
        with utilo.file.securewrapper.open(image, mode='rb') as fp:
            image = fp.read()
        # TODO: IS BYTESIO REALLY REQUIRED
        image = io.BytesIO(image)
        response = flask.send_file(image, mimetype='image')
        return response
    # Hint: contextmanager does not work here
    response = flask.send_file(
        open(image, mode='rb'),  # pylint:disable=R1732
        mimetype='image',
    )
    return response


@result_.route('/view/failure')
def failure():
    return flask.render_template('view/failure.html')
