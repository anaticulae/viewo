# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask

import viewo.result.data
import viewo.result.json
import viewo.waiting.data
import viewo.waiting.fastview

waiting_ = flask.Blueprint('waiting', __name__)  # pylint:disable=C0103


@waiting_.route('/waiting/<string:process>')
def waiting_view(process):
    return flask.render_template('waiting/index.html', process=process)


@waiting_.route('/waiting/fastview/<string:process>')
def waiting_view_fastview(process):
    return flask.render_template('waiting/fastview.html', process=process)


@waiting_.route('/waiting/resultview/<string:process>')
def waiting_view_resultview(process):
    rendered = flask.render_template(
        'result/index.html',
        process=process,
        waiting=True,
    )
    return rendered


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
    loaded = viewo.waiting.data.status(process)
    if not loaded:
        return '{}'
    dumped = viewo.waiting.data.jsonify(loaded)
    return dumped


@waiting_.route('/waiting/fastview/status/<string:process>')
def waiting_fastview_status(process: str):
    loaded = viewo.waiting.fastview.load_fastview_result(process)
    if loaded is None:
        return '{}'
    dumped = viewo.waiting.fastview.fastviewstatus_tojson(loaded)
    return dumped


@waiting_.route('/waiting/resultview/status/<string:process>')
def waiting_resultview_status(process: str):
    loaded = viewo.result.data.load_resultview_result(process)
    if loaded is None:
        return '{}'

    pagesentences = viewo.result.loader.load_sentences_fromprocess(process)
    footnotes = viewo.result.loader.load_footnotes_fromprocess(process)
    doctextstyle = viewo.result.loader.load_doctextstyle_fromprocess(process)

    dumped = viewo.result.json.tojson(
        loaded,
        pagesentences=pagesentences,
        footnotes=footnotes,
        doctextstyle=doctextstyle,
    )
    return dumped
