# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json
import os

import configo
import flask
import link
import link.job
import werkzeug.utils

api_documents = flask.Blueprint('api_documents', __name__)  # pylint:disable=C0103


@api_documents.route('/documents', methods=['GET'])
def documents():
    collected = all_documents()
    dumped = json.dumps({
        'documents': collected,
    })
    return dumped


@api_documents.route('/documents/<string:documentid>', methods=['GET'])
def document_get(documentid: str):
    """Recieve document information selected by documentid. If document
    does not exists, 404 Error will be raised."""
    documentpath = link.document(documentid)  # pylint:disable=E1101
    if documentpath is None:
        return notfound(f'could not locate `{documentid}`')
    source = os.path.join(link.document(documentid), link.JOB_FILE_NAME)  # pylint:disable=E1101
    if not os.path.exists(source):
        return notfound(f'could not locate `{documentid}` {source}')
    # TODO: REPLACE WITH JSON METHOD
    loaded = job_toraw(link.load_job(source))
    dumped = json.dumps({
        'document': loaded,
    })
    return dumped


@api_documents.route('/documents', methods=['POST'])
def document_create() -> str:
    if not flask.request.files:
        return bad('missing `file` field')

    pdf = flask.request.files['file']
    filename = werkzeug.utils.secure_filename(pdf.filename)
    if pdf.filename == '':
        # if user does not select file, browser also submit an empty part
        # without filename
        return bad('empty `file` field')

    todo = link.create_todo(pdf, filename)
    _, resource = os.path.split(todo)

    result = success(
        document=flask.url_for(
            f'api_documents.document_get',
            documentid=resource,
        ),
        link=flask.url_for('writing.view_result', document=resource),
    )
    return result


@api_documents.route('/documents/<string:documentid>', methods=['DELETE'])
def document_delete(documentid) -> str:
    current = link.current(documentid)
    if current is None:
        return notfound(f'"{documentid}" does not exists')
    if current == link.ProcessState.UNDEFINED:
        return internal('unexpected state')
    if current == link.ProcessState.DELETED:
        return bad('resource was already deleted')
    link.delete(documentid)
    return success(f'deleted: {documentid}')


def all_documents():
    todos, dones = link.collect_jobs(configo.share())
    result = []
    for todo in todos:
        dumped = job_toraw(todo)
        result.append(dumped)
    for done in dones:
        dumped = job_toraw(done)
        result.append(dumped)
    return result


def job_toraw(info: link.JobInfo) -> dict:
    result = {
        'title': info.title,
        'date': info.date,
        'result': link.job.findingstatus_toraw(info.result),
        'index': info.index,
        'done': info.done,
    }
    if info.password:
        result['password'] = 'XXXXXXXXXX'  # info.password
    if info.hashlink:
        result['hashlink'] = info.hashlink
    return result


def success(message: str = 'completed', **args):
    result = flask.jsonify({
        'message': message,
        **args,
    })
    return result, 200


def notfound(message: str):
    result = flask.jsonify({
        'error': 'not found',
        'message': message,
    })
    return result, 404


def bad(message: str):
    result = flask.jsonify({
        'error': 'bad request',
        'message': message,
    })
    return result, 400


def internal(message: str):
    result = flask.jsonify({
        'error': 'internal',
        'message': message,
    })
    return result, 500
