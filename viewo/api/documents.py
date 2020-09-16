# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json

import configo
import flask
import link
import link.job

api_documents = flask.Blueprint('api_documents', __name__)  # pylint:disable=C0103


@api_documents.route('/documents', methods=['GET'])
def documents():
    collected = all_documents()
    dumped = json.dumps({
        'documents': collected,
    })
    return dumped


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
