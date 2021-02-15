# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import json
import os

import flask
import iamraw.caption
import link
import link.job
import utila

import viewo.path
import viewo.result.json
import viewo.result.loader
import viewo.waiting


def all_documents(userid: str = None):
    todos, dones = link.collect_jobs(
        viewo.path.common(),
        skip_removed=True,
        owner=userid,
    )
    result = []
    ready_indexes = {item.name for item in dones}

    for todo in todos:
        if todo.name in ready_indexes:
            continue
        todo.state = state(todo.name)
        result.append(todo)
    for done in dones:
        # set done flag
        done.done = True
        done.state = state(done.name)
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
        'name': info.name,
        'done': info.done,
        'state': info.state,
        'owner': info.owner,
    }
    if info.password:
        result['password'] = 'XXXXXXXXXX'  # info.password
    if info.hashlink:
        result['hashlink'] = info.hashlink
    return result


def state(documentid: str) -> int:
    current = link.current(documentid)
    if current is None:
        return -2
    converted = link.State.fromstate(current)
    return int(converted)


def footnotes(documentid):
    loaded = viewo.result.loader.load_footnotes_fromprocess(documentid)
    raw = viewo.result.json.footnotes_tojson(loaded)
    simple = {'resource': viewo.api.utils.simple_recursive(raw, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.footnotes_get',
        documentid=documentid,
    )
    return simple


def style(documentid):
    loaded = viewo.result.loader.load_doctextstyle_fromprocess(documentid)
    raw = viewo.result.json.doctextstyle_tojson(loaded)
    simple = {'resource': viewo.api.utils.simple_recursive(raw, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.docstyle_get',
        documentid=documentid,
    )
    return simple


def captions(documentid):
    loaded = viewo.result.loader.load_captions_fromprocess(documentid)
    raw = iamraw.caption.pagecaptions_toraw(loaded) if loaded else []
    simple = {'resource': viewo.api.utils.simple_recursive(raw, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.captions_get',
        documentid=documentid,
    )
    return simple


def bibliography(documentid):
    loaded = viewo.result.loader.load_bibliography_fromprocess(documentid)
    # raw = iamraw.caption.pagecaptions_toraw(loaded) if loaded else []
    raw = utila.flatten(loaded) if loaded else []
    simple = {'resource': viewo.api.utils.simple_recursive(raw, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.bibliography_get',
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


def links(documentid):
    loaded = viewo.result.loader.load_links_fromprocess(documentid)
    raw = viewo.api.utils.simple_recursive(loaded, not_none=False)
    simple = {'resource': raw}
    simple['uri'] = flask.url_for(
        'api_documents.links_get',
        documentid=documentid,
    )
    return simple


def document_info(documentid) -> dict:
    docpath = link.document(documentid)
    source = os.path.join(docpath, link.JOB_FILE_NAME)
    if not os.path.exists(source):
        return None
    loaded = viewo.api.documents.utils.job_toraw(link.load_job(source))

    # append document length
    pdfinfo = os.path.join(docpath, viewo.waiting.VERIFY)
    if os.path.exists(pdfinfo):
        pdfinfo = json.loads(utila.file_read(pdfinfo))
        # TODO: REPLACE WITH JSON METHOD
        loaded['pages'] = pdfinfo['pages']
    return loaded
