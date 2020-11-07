"use strict";

const OVERVIEW = -1
const FOOTNOTES = 1025
const CAPTIONS = 1026
const DOCSTYLE = 1027
const PROPERTIES = 1028

const SPECIALCONTENT = 'NONE'
const SPECIALCONTENT_EMPTY = 'NONE_EMPTY'

class DocumentService {
    constructor() {
        this.documentid = null
        this.content = null
        this.pagenumbers = null
    }

    update(documentid) {
        this.documentid = documentid
        this.content = []
        this.update_pagenumbers()
        this.update_pagecontent(null, function ready() {
            service.update_footnotes()
            service.update_captions()
            service.update_properties()
            service.update_docstyle()
        })
    }

    update_pagenumbers() {
        rpc(`/documents/${this.documentid}`, function (response) {
            service.pagenumbers = response.document.pages

            service.content = defaultpages(service.pagenumbers)

            navigator.update_page_navigator()
            resultview.show_page(0)
            base.show_done()
        })
    }

    update_footnotes() {
        rpc(`/documents/${this.documentid}/footnotes`, function (response) {
            if (response.footnotes.resource.length) {
                update_content(FOOTNOTES, response.footnotes.resource)
            } else {
                update_content(FOOTNOTES, SPECIALCONTENT_EMPTY)
            }
            navigator.update_page_navigator()
        })
    }

    update_captions() {
        rpc(`/documents/${this.documentid}/captions`, function (response) {
            let captions = response.captions.resource
            if (captions.length) {
                update_content(CAPTIONS, captions)
            } else {
                update_content(CAPTIONS, SPECIALCONTENT_EMPTY)
            }
            navigator.update_page_navigator()
        })
    }

    update_properties() {
        rpc(`/documents/${this.documentid}/properties`, function (response) {
            let properties = response.properties.resource
            update_content(PROPERTIES, properties)
            navigator.update_page_navigator()
        })
    }

    update_docstyle() {
        rpc(`/documents/${this.documentid}/style`, function (response) {
            let style = response.style.resource
            update_content(DOCSTYLE, style)
            navigator.update_page_navigator()
        })
    }

    update_pagecontent(current = null, callback = null) {
        if (current == null) {
            current = 0
        }
        let end = current + 5
        rpc(`/documents/${this.documentid}/pages?range=${current}:${end}`, function (response) {
            for (let page of response.pages.html) {
                update_content(current, page)
                current += 1
            }
            if (response.pages.html.length) {
                if (callback != null) {
                    callback()
                }
            } else {
                // NO CONTENT WAS PROVIDED BY THIS CALL
                // TODO: INFORM ABOUT LOADING ERROR?
            }
        })
    }

    get pages() {
        if (this.empty) {
            return []
        }
        let result = []
        for (let item of this.content) {
            result.push(item)
        }
        return result
    }

    get empty() {
        return this.content == null || this.content.length == 0
    }

}

function update_content(index, content) {
    index = service.content.findIndex(s => (s.page == index))
    service.content[index].content = content
}

function page_content(pagenumber) {
    let selected = service.content.find(s => (s.page == pagenumber))
    return selected.content
}

function page(pagenumber) {
    let selected = service.content.find(s => (s.page == pagenumber))
    return selected
}

function empty(content) {
    return content == SPECIALCONTENT || content == SPECIALCONTENT_EMPTY
}

function defaultpages(pagenumbers) {
    let result = []
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': -1,
        'title': 'Übersicht',
    })

    for (let page = 0; page < pagenumbers; page++) {
        result.push({
            'content': null,
            'findings': null,
            'page': page,
            'title': page + 1,
        })
    }

    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': FOOTNOTES,
        'title': 'Fußnoten',
    })
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': CAPTIONS,
        'title': 'Unterschriften',
    })
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': DOCSTYLE,
        'title': 'Darstellung',
    })
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': PROPERTIES,
        'title': 'Eigenschaften',
    })
    return result
}

const service = new DocumentService()
