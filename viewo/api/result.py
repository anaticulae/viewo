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
import utila

result_ = flask.Blueprint('result', __name__)  # pylint:disable=C0103


@result_.route('/result', defaults={'documentid': None})
@result_.route('/result/<string:documentid>')
def view_result(documentid: str = None):
    if not documentid:
        return flask.redirect(flask.url_for('documents.view_documents'))

    invalid_document = not os.path.exists(link.ready(documentid))
    if invalid_document:
        return flask.redirect('result/failure')

    rendered = flask.render_template(
        'result/index.html',
        process=documentid,
        waiting=False,
    )
    return rendered


@result_.route('/result/<string:documentid>/<string:image>')
def view_images(documentid: str = None, image: str = None):
    source = link.ready(documentid)
    invalid_document = not os.path.exists(source)
    if invalid_document:
        utila.error(f'could not load document: {source}')
        return flask.redirect('result/failure')

    image = os.path.join(source, 'result/view/', image)
    if not os.path.exists(image):
        utila.error(f'could not load image: {image}')
        return flask.redirect('result/failure')

    # Hint: contextmanager does not work here
    response = flask.send_file(open(image, mode='rb'), mimetype='image')
    return response


@result_.route('/result/failure')
def failure():
    return flask.render_template('result/failure.html')
