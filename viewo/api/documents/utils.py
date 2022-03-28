# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import iamraw.caption
import utila

import viewo.result.json
import viewo.result.loader
import viewo.result.loader.footnotes
import viewo.result.loader.pagenumbers


def footnotes(documentid):
    loaded = viewo.result.loader.footnotes.load_fromdocumentid(documentid)
    raw = viewo.result.json.footnotes_tojson(loaded)
    simple = {'resource': utila.simplify(raw, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.footnotes_get',
        documentid=documentid,
    )
    return simple


def style(documentid):
    loaded = viewo.result.loader.load_doctextstyle_fromdocumentid(documentid)
    raw = viewo.result.json.doctextstyle_tojson(loaded)
    simple = {'resource': utila.simplify(raw, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.docstyle_get',
        documentid=documentid,
    )
    return simple


def captions(documentid):
    loaded = viewo.result.loader.load_captions_fromdocumentid(documentid)
    raw = iamraw.caption.pagecaptions_toraw(loaded) if loaded else []
    simple = {'resource': utila.simplify(raw, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.captions_get',
        documentid=documentid,
    )
    return simple


def bibliography(documentid):
    loaded = viewo.result.loader.load_bibliography_fromdocumentid(documentid)
    # raw = iamraw.caption.pagecaptions_toraw(loaded) if loaded else []
    raw = loaded.references if loaded else []
    simple = {'resource': utila.simplify(raw, not_none=False)}
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
    loaded = viewo.result.loader.load_links_fromdocumentid(documentid)
    if loaded is None:
        # no extracted links
        loaded = []
    raw = utila.simplify(loaded, not_none=False)
    simple = {'resource': raw}
    simple['uri'] = flask.url_for(
        'api_documents.links_get',
        documentid=documentid,
    )
    return simple


def pagenumbers(documentid):
    loaded = viewo.result.loader.pagenumbers.load_fromdocumentid(documentid)
    simple = {'resource': utila.simplify(loaded, not_none=False)}
    simple['uri'] = flask.url_for(
        'api_documents.pagenumbers_get',
        documentid=documentid,
    )
    return simple
