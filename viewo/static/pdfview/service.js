"use strict";

const OVERVIEW = -1
const BIBLIOGRAPHY = 1025
const FOOTNOTES = 1026
const HYPERLINKS = 1027
const CAPTIONS = 1028
const PROPERTIES = 1029
const DOCSTYLE = 1030
const FINDINGS = 1031
const CHECKLIST = 1032
const SCORE = 1033

const SPECIALCONTENT = 'NONE'
const SPECIALCONTENT_EMPTY = 'NONE_EMPTY'

class DocumentService {
    constructor() {
        this.documentid = null
        this.content = null
        this.pagenumbers = null
        this.waiting = false
        this.fastfindings = []
        this.pdf = null
    }

    update(documentid) {
        this.documentid = documentid
        this.content = []
        this.fastfindings = []
        this.update_pagenumbers()
        this.update_pdf()
        this.update_pagecontent(null, function ready() {
            service.update_overview()
            service.update_footnotes()
            service.update_fastfindings()
            service.update_captions()
            service.update_properties()
            service.update_docstyle()
            service.update_hyperlinks()
            service.update_bibliography()
            service.update_findings()
            service.update_navigator_labels()
        })
    }

    update_pagenumbers() {
        rpc(`/documents/${this.documentid}`, function (response) {
            service.pagenumbers = response.document.pages
            service.content = defaultpages(service.pagenumbers)
            navigator.create_pagenavigator(service.pages)
            resultview.show_page(0)
            base.show_done()
        }, function () {
            base.show_error()
        })
    }

    update_navigator_labels() {
        rpc(`/documents/${this.documentid}/pagenumbers`, function (response) {
            let labels = response.pagenumbers.resource
            navigator.update_labels(labels)
        }, function () {
            base.show_error()
        })

    }
    update_pdf() {
        if (MODERN == false) {
            return
        }
        let url = `/api/v0/documents/${this.documentid}/pdf`
        let loadingTask = pdfjsLib.getDocument(url);
        loadingTask.promise.then(function (pdf) {
            service.pdf = pdf
            resultview.show_pdf(0)
        })
    }

    update_fastfindings() {
        rpc(`/documents/${this.documentid}/fastfindings`, function (response) {
            service.fastfindings = response
        })
    }

    update_footnotes() {
        rpc(`/documents/${this.documentid}/footnotes`, function (response) {
            let footnotes = response.footnotes.resource
            if (response.footnotes.resource.length) {
                update_content(FOOTNOTES, footnotes)
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

    update_hyperlinks() {
        rpc(`/documents/${this.documentid}/links`, function (response) {
            let links = response.links.resource
            if (links.length) {
                update_content(HYPERLINKS, links)
            } else {
                update_content(HYPERLINKS, SPECIALCONTENT_EMPTY)
            }
            navigator.update_page_navigator()
            // TODO: ADD TABLE CHANGE LISTENER
            hyperlinksview.update_content(links)
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

    update_bibliography() {
        rpc(`/documents/${this.documentid}/bibliography`, function (response) {
            let bibs = response.bibliography.resource
            if (bibs.length) {
                update_content(BIBLIOGRAPHY, bibs)
            } else {
                update_content(BIBLIOGRAPHY, SPECIALCONTENT_EMPTY)
            }
            navigator.update_page_navigator()
            bibliographyview.update_content(bibs)
        })
    }

    update_findings() {
        rpc(`/documents/${this.documentid}/findings`, function (response) {
            let findings = response.findings.pagefindings
            if (findings.length) {
                update_content(FINDINGS, findings)
                for (let findingpage of findings) {
                    page(findingpage.pdfpage).findings = findingpage.content
                }
            } else {
                update_content(FINDINGS, SPECIALCONTENT_EMPTY)
            }
            navigator.update_page_navigator()
            findingview.update_content(findings)
            statuscounter.update()
        })
    }

    update_overview() {
        // TODO: IMPROVE PAGES SYNTAX
        rpc(`/documents/${this.documentid}/findings?pages=_1:0`, function (response) {
            let findings = response.findings.pagefindings
            if (findings.length) {
                update_content(OVERVIEW, findings)
            } else {
                update_content(OVERVIEW, SPECIALCONTENT_EMPTY)
            }
            navigator.update_page_navigator()
        })
    }

    update_pagecontent(current = null, callback = null) {
        if (current == null) {
            current = 0
        }
        let end = current + 5
        let callrange = special_pattern(current, end)
        rpc(`/documents/${this.documentid}/pageviews?pages=${callrange}`, function (response) {
            for (let html of response.pageviews.html) {
                update_content(current, html)
                current += 1
            }
            // start download findings
            // service.update_pagefindings(current, function () {
            //     findingbox.update_findings(current)
            // })
            if (response.pageviews.html.length) {
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
        let callrange = special_pattern(current, current + 5)
        rpc(`/documents/${this.documentid}/findings?pages=${callrange}`, function (response) {
            let pagerange = response.findings.pages
            empty_findings(pagerange)
            let findings = response.findings.pagefindings
            for (let pagefindings of findings) {
                update_findings(pagefindings.pdfpage, pagefindings.content)
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
        if (current == undefined) {
            return []
        }
        if (current.findings == null) {
            // signal that findings are already called
            current.findings = []
            // update findings
            service.update_pagefindings(pagenumber)
        }
        return current.findings
    }

    smooth(pagenumber, lookaround = 5) {
        // before before and after
        if (this.waiting) {
            return
        }
        let index = service.content.findIndex(s => (s.page == pagenumber))
        let start = Math.max(0, index - lookaround)
        let end = Math.min(service.content.length, index + lookaround)
        let selected = service.content.slice(start, end)
        let range = []
        for (let item of selected) {
            if (item.findings == null && item.hasOwnProperty('findings')) {
                range.push(item.page)
            }
        }
        if (range.length == 0) {
            return
        }
        this.waiting = true
        start = Math.min(...range)
        end = Math.max(...range)
        let callrange = special_pattern(start, end)
        rpc(`/documents/${this.documentid}/findings?pages=${callrange}`, function (response) {
            let pagerange = response.findings.pages
            empty_findings(pagerange)
            let findings = response.findings.pagefindings
            for (let pagefindings of findings) {
                update_findings(pagefindings.pdfpage, pagefindings.content)
            }
            service.waiting = false
        })
    }

    finding_update(findingid, status) {
        // DIRTY, unite with fastfindings_solve
        for (let page of this.content) {
            if (page.findings == undefined) {
                continue
            }
            for (let finding of page.findings) {
                if (finding.number == findingid) {
                    finding.solution.status = status
                    break
                }
            }
        }
        this.fastfindings_solve(findingid, status)
    }

    fastfindings_solve(findingid, status) {
        // Removes finding when finding is solved or deleted
        if (![DONE, REMOVED].includes(status)) {
            // not remove or done
            return
        }
        for (let page of this.fastfindings) {
            if (page.content == undefined) {
                continue
            }
            let done = page.content.indexOf(findingid)
            if (done != -1) {
                // page.content.remove(done)
                page.content.splice(findingid)
                break
            }
        }
        statuscounter.update()
    }
}

const special_pattern = function (start, end) {
    start = String(start).replace('-', '_')
    end = String(end).replace('-', '_')
    if (start == end) {
        return start
    }
    return `${start}:${end}`
}

const empty_findings = function (pagerange) {
    let splitted = pagerange.split(':')
    let start = parseInt(splitted[0])
    let end = parseInt(splitted[1])
    end = Math.min(end, service.pagenumbers - 1)
    for (let index = start; index <= end; index++) {
        update_findings(index, [])
    }
}

const update_content = function (index, content) {
    index = service.content.findIndex(s => (s.page == index))
    service.content[index].content = content
}

const update_findings = function (index, findings) {
    let current = page(index)
    current.findings = findings
}

const page_content = function (pagenumber) {
    let selected = service.content.find(s => (s.page == pagenumber))
    return selected.content
}

const page = function (pagenumber) {
    let selected = service.content.find(s => (s.page == pagenumber))
    return selected
}

const empty = function (content) {
    return content == SPECIALCONTENT || content == SPECIALCONTENT_EMPTY
}

const visible_findings = function (pagenumber) {
    let selected = page(pagenumber)
    if (selected == undefined || selected.findings == undefined) {
        return []
    }
    let findings = selected.findings.filter(s => visible(s))
    return findings
}

const open_findings = function (pagenumber) {
    let selected = service.fastfindings.filter(s => s.page == pagenumber && s.content.length > 0)
    return selected.length > 0
}

const next_page = function (pagenumber) {
    let index = service.content.findIndex(s => (s.page == pagenumber))
    index += 1
    if (index == service.content.length) {
        return service.content[0].page
    }
    return service.content[index].page
}

const next_page_visible = function (pagenumber) {
    let current = pagenumber
    do {
        current = next_page(current)
    } while (empty(page_content(current)) && current != pagenumber)
    return current
}

const previous_page = function (pagenumber) {
    let index = service.content.findIndex(s => (s.page == pagenumber))
    if (index == 0) {
        return service.content[service.content.length - 1].page
    }
    return service.content[index - 1].page
}

const previous_page_visible = function (pagenumber) {
    let current = pagenumber
    do {
        current = previous_page(current)
    } while (empty(page_content(current)) && current != pagenumber)
    return current
}

const defaultpages = function (pagenumbers) {
    let result = []
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': OVERVIEW,
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
        'page': BIBLIOGRAPHY,
        'title': 'Bibliographie',
    })
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': FOOTNOTES,
        'title': 'Fußnoten',
    })
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': HYPERLINKS,
        'title': 'Hyperlinks',
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
    result.push({
        'content': SPECIALCONTENT_EMPTY,
        'page': FINDINGS,
        'title': 'Fehlerübersicht',
    })
    result.push({
        'content': 'TODO',
        'page': CHECKLIST,
        'title': 'Checkliste',
    })
    result.push({
        'content': 'Layout, Writing Style, Bibs',
        'page': SCORE,
        'title': 'CIW-Score',
    })
    return result
}

const service = new DocumentService()
