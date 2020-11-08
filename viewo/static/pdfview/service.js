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
            for (let html of response.pages.html) {
                update_content(current, html)
                current += 1
            }
            // start download findings
            service.update_pagefindings(current, function () {
                findingbox.update_findings(current)
            })
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

    update_pagefindings(current = null, callback = null) {
        if (current == null) {
            current = 0
        }
        let end = current + 5
        rpc(`/documents/${this.documentid}/findings?pages=${current}:${end}`, function (response) {
            let findings = response.findings.pages
            for (let pagefindings of findings) {
                update_findings(pagefindings.page, pagefindings.content)
            }
            if (findings.length) {
                if (callback != null) {
                    callback()
                }
            } else {
                // NO FINDINGS WHERE PROVIDED BY THIS CALL
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

    pagefindings(pagenumber) {
        let current = page(pagenumber)
        if (current.findings == null) {
            // signal that findings are already called
            current.findings = []
            // update findings
            service.update_pagefindings(pagenumber)
        }
        return current.findings
    }
}

function update_content(index, content) {
    index = service.content.findIndex(s => (s.page == index))
    service.content[index].content = content
}

function update_findings(index, findings) {
    let current = page(index)
    current.findings = findings
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

function visible_findings(pagenumber) {
    let selected = page(pagenumber)
    if (selected == undefined || selected.findings == undefined) {
        return []
    }
    let findings = selected.findings.filter(s => visible(s))
    return findings
}

function next_page(pagenumber) {
    let index = service.content.findIndex(s => (s.page == pagenumber))
    index += 1
    if (index == service.content.length) {
        return service.content[0].page
    }
    return service.content[index].page
}

function next_page_visible(pagenumber) {
    let current = pagenumber
    do {
        current = next_page(current)
    } while (empty(page_content(current)) && current != pagenumber)
    return current
}

function previous_page(pagenumber) {
    let index = service.content.findIndex(s => (s.page == pagenumber))
    if (index == 0) {
        return service.content[service.content.length - 1].page
    }
    return service.content[index - 1].page
}

function previous_page_visible(pagenumber) {
    let current = pagenumber
    do {
        current = previous_page(current)
    } while (empty(page_content(current)) && current != pagenumber)
    return current
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
