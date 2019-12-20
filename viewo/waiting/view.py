# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import flask

import viewo.waiting.data

waiting_ = flask.Blueprint('waiting', __name__)  # pylint:disable=C0103


@waiting_.route('/waiting/<string:process>')
def waiting_view(process):
    return flask.render_template('waiting/index.html', process=process)


@waiting_.route('/waiting/fastview/<string:process>')
def waiting_view_fastview(process):
    return flask.render_template('waiting/fastview.html', process=process)


@waiting_.route('/waiting/validation', defaults={'process': None})
@waiting_.route('/waiting/validation/<string:process>')
def waiting_view_validation(process):
    validated = viewo.waiting.data.load_validation_result(process)
    if process is None or validated is None:
        return flask.redirect(flask.url_for('result.failure'))

    rendered = flask.render_template(
        'waiting/validation.html',
        process=process,
        validation_result=validated,
    )
    return rendered


@waiting_.route('/waiting/status/<string:process>')
def waiting_status(process: str):
    try:
        process = str(process)
    except UnicodeDecodeError:
        return '{}'
    if not process:
        return '{}'
    loaded = viewo.waiting.data.status(process)
    if not loaded:
        return '{}'
    dumped = viewo.waiting.data.jsonify(loaded)
    return dumped


@waiting_.route('/waiting/fastview/status/<string:process>')
def waiting_fastview_status(process: str):
    loaded = viewo.waiting.data.load_fastview_result(process)
    if loaded is None:
        return '{}'
    dumped = viewo.waiting.data.fastviewstatus_tojson(loaded)
    return dumped
