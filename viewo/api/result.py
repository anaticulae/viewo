# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import link
import utila

result_ = flask.Blueprint('result', __name__)  # pylint:disable=C0103


@result_.route('/view', defaults={'documentid': None})
@result_.route('/view/<string(length=16):documentid>')
def view_result(documentid: str = None):
    if not documentid:
        return flask.redirect(flask.url_for('documents.view_documents'))

    invalid_document = not os.path.exists(link.ready(documentid))
    if invalid_document:
        return flask.redirect('view/failure')

    rendered = flask.render_template(
        'view/index.html',
        process=documentid,
        waiting=False,
    )
    return rendered


@result_.route('/view/<string(length=16):documentid>/<string:image>')
def view_images(documentid: str = None, image: str = None):
    source = link.ready(documentid)
    invalid_document = not os.path.exists(source)
    if invalid_document:
        utila.error(f'could not load document: {source}')
        return flask.redirect('view/failure')

    image = os.path.join(source, 'result/view/', image)
    if not os.path.exists(image):
        utila.error(f'could not load image: {image}')
        return flask.redirect('view/failure')

    # Hint: contextmanager does not work here
    response = flask.send_file(open(image, mode='rb'), mimetype='image')
    return response


@result_.route('/view/failure')
def failure():
    return flask.render_template('view/failure.html')
