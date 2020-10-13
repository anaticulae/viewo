# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import flask
import iamraw.caption
import link
import link.job

import viewo.result.json
import viewo.result.loader


def all_documents():
    todos, dones = link.collect_jobs(configo.share())
    result = []
    ready_indexes = {item.index for item in dones}

    for todo in todos:
        if todo.index in ready_indexes:
            continue
        result.append(todo)
    for done in dones:
        result.append(done)

    result = sorted(
        result,
        key=lambda item: link.sortable_date(item.date),
        reverse=True,
    )
    result = [job_toraw(job) for job in result]
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


def footnotes(documentid):
    loaded = viewo.result.loader.load_footnotes_fromprocess(documentid)
    raw = viewo.result.json.footnotes_tojson(loaded)
    simple = {'resource': viewo.api.utils.simple_recursive(raw)}
    simple['uri'] = flask.url_for(
        'api_documents.footnotes_get',
        documentid=documentid,
    )
    return simple


def style(documentid):
    loaded = viewo.result.loader.load_doctextstyle_fromprocess(documentid)
    raw = viewo.result.json.doctextstyle_tojson(loaded)
    simple = {'resource': viewo.api.utils.simple_recursive(raw)}
    simple['uri'] = flask.url_for(
        'api_documents.docstyle_get',
        documentid=documentid,
    )
    return simple


def captions(documentid):
    loaded = viewo.result.loader.load_captions_fromprocess(documentid)
    raw = iamraw.caption.pagecaptions_toraw(loaded) if loaded else []
    simple = {'resource': viewo.api.utils.simple_recursive(raw)}
    simple['uri'] = flask.url_for(
        'api_documents.captions_get',
        documentid=documentid,
    )
    return simple


def properties(documentid):
    raw = viewo.result.json.properties_tojson({})
    simple = {'resource': raw}
    simple['uri'] = flask.url_for(
        'api_documents.properties_get',
        documentid=documentid,
    )
    return simple
