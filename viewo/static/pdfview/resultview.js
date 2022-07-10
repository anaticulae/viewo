/*
*
*/

class ResultView {

    constructor() {
        this.pageopen = null
        this.error_selected = null
        this.hide_all()
    }

    overlay_finding(findingid) {
        if (this.pageopen < 0) {
            return
        }
        if (findingid == null) {
            let source = pdfpage_source(this.pageopen)
            $("#show_page").attr("src", source);
            return
        }
        let documentid = SERVICE.documentid
        let image = `${documentid}/${findingid}.png`
        $("#show_page").attr("src", image);
    }

    reset_finding_selector(pagenumber) {
        this.pageopen = pagenumber
        this.error_selected = 0
        findingbox.paged = 0
    }


    hide_all() {
        $('#pdfview_bibliography').hide()
        $('#pdfview_captions').hide()
        $('#pdfview_content').hide()
        $('#pdfview_docstyle').hide()
        $('#pdfview_findings').hide()
        $('#pdfview_footnotes').hide()
        $('#pdfview_hyperlinks').hide()
        $('#pdfview_overview').hide()
        $('#pdfview_properties').hide()
        $('#pdfview_checklist').hide()
    }

    show_overview() {
        $('#pdfview_overview').show()
        let overview = $('#pdfview_overview_content')
        overview.html('')
        let content = page_content(OVERVIEW)[0].content
        for (let finding of content) {
            if (visible(finding) == false) {
                continue
            }
            let solution = finding.solution
            let del = `delete_${finding.number}`
            let done = `done_${finding.number}`
            let content = `
            <div class="flex_content" id="flex_content_${finding.number}">
                <h4>${solution.title}</h4>
                <div class="error_message">${solution.description}</div>
                <p class="error_options">
                    <button type="button" id="${del}">
                        <img src="/static/images/view/right.png" alt="done" width="100%" height="100%" />
                    </button>
                    <button type="button" id="${done}">
                        <img src="/static/images/view/trash.png" alt="delete" width="100%" height="100%" />
                    </button>
                </p>
            </div>
            `
            $('#pdfview_overview_content').append(content)
            $(`#${del}`).click(function () {
                RESULTVIEW.update_finding(finding.number, REMOVED)
                $(`#flex_content_${finding.number}`).hide()
            });
            $(`#${done}`).click(function () {
                RESULTVIEW.update_finding(finding.number, DONE)
                $(`#flex_content_${finding.number}`).hide()
            });
        }
    }

    show_footnotes(update = false) {
        $('#pdfview_footnotes').show()
        let list = $('#pdfview_footnotes_list')
        if (list[0].rows.length > 0 && !update) {
            return
        }
        list.html('')
        let footnotes = page_content(FOOTNOTES)
        if (empty(footnotes)) {
            return
        }
        let current = null
        let index = 0
        for (let footnote of footnotes) {
            let status = '✔'
            if (footnote.error != '') {
                status = '✖'
            }
            if (current != null && current != footnote.pdfpage) {
                list.append('<tr><td style="border-top:solid black 1px;" colspan="4"></td></tr>')
            }
            current = footnote.pdfpage
            let href = `footnote_openpage${index}`
            let row = `
            <tr>
            <td class="center top">${footnote.number}</td>
            <td class="expand"><span id="${href}" class="click underline">${footnote.title}</span></td>
            <td class="center top">${footnote.page}</td>
            <td class="center top">${status}</td>
            </tr>`
            list.append(row)
            $(`#${href}`).click(function () {
                $(`#openpage${footnote.pdfpage}`).click()
            });
            index += 1
        }
    }

    show_captions(update = false) {
        $('#pdfview_captions').show()
        let list = $('#pdfview_captions_list')
        if (list[0].rows.length > 0 && !update) {
            return
        }
        list.html('')
        let captions = page_content(CAPTIONS)
        if (empty(captions)) {
            return
        }
        let current = null
        let index = 0
        for (let page of captions) {
            for (let item of page.captions) {
                let nr = index + 1
                let status = '✔'
                if (item.error != '') {
                    status = '✖'
                }
                if (current != null && current != item.page) {
                    list.append('<tr><td style="border-top:solid black 1px;" colspan="4"></td></tr>')
                }
                current = item.page
                let href = `caption_openpage${index}`
                let row = `
            <tr>
            <td class="center top">${nr}</td>
            <td class="expand"><span id="${href}" class="click underline">${item.raw}</span></td>
            <td class="center top">${page.page}</td>
            <td class="center top">${status}</td>
            </tr>`
                list.append(row)
                $(`#${href}`).click(function () {
                    $(`#openpage${page.pdfpage}`).click()
                });
                index += 1
            }
        }
    }

    show_hyperlinks() {
        $('#pdfview_hyperlinks').show()
    }

    show_bibliography() {
        $('#pdfview_bibliography').show()
    }

    show_findings() {
        $('#pdfview_findings').show()
    }

    show_checklist() {
        $('#pdfview_checklist').show()
    }

    show_pdf_properties() {
        let properties = page_content(PROPERTIES)
        pdfview_properties.update(properties)
        pdfview_properties.show()
    }

    show_docstyle() {
        let docstyle = page_content(DOCSTYLE)
        pdfview_docstyle.update(docstyle)
        pdfview_docstyle.show()
    }

    get current_page() {
        return RESULTVIEW.pageopen
    }

    get current_finding() {
        if (RESULTVIEW.error_selected == null) {
            return null
        }
        return parseInt(RESULTVIEW.error_selected)
    }

    get available_pages() {
        if (SERVICE.content == undefined) {
            return 0
        }
        return SERVICE.content.length
    }

    get findings() {
        if (SERVICE.content == undefined) {
            return []
        }
        if (SERVICE.content.length <= RESULTVIEW.current_page) {
            return []
        }
        let result = []
        for (let item of SERVICE.content[RESULTVIEW.current_page].findings) {
            result.push(item)
        }
        return result
    }

    get selected_finding() {
        let findings = visible_findings(RESULTVIEW.current_page)
        // let findings = page(RESULTVIEW.current_page).findings
        if (findings == undefined) {
            return null
        }
        if (this.current_finding < findings.length) {
            return findings[RESULTVIEW.current_finding]
        }
        return null
    }

    get get_next_finding() {
        let findings = visible_findings(RESULTVIEW.current_page)
        if (findings.length == 0) {
            return null
        }
        let current_plus = RESULTVIEW.current_finding + 1
        if (current_plus == findingbox.finding_max) {
            current_plus = 0
        }
        for (let index = current_plus; index < findingbox.finding_max; index++) {
            if (visible(findings[index]) == false) {
                continue
            }
            if (findings[index].solution.status <= SELECTED) {
                return index
            }
        }
        return null
    }

    get get_prev_finding() {
        let findings = visible_findings(RESULTVIEW.current_page)
        if (findings.length == 0) {
            return null
        }
        let current_minus = RESULTVIEW.current_finding - 1
        if (current_minus < 0) {
            current_minus = findingbox.finding_max - 1
        }
        for (let index = current_minus; index >= 0; index--) {
            if (visible(findings[index]) == false) {
                continue
            }
            if (findings[index].solution.status <= SELECTED) {
                return index
            }
        }
        return null
    }

    update_current_finding_status(status) {
        if (this.selected_finding == null) {
            return
        }
        let findingid = this.selected_finding.number
        this.selected_finding.solution.status = status // remove finding
        this.update_finding(findingid, status)
        this.update_current_finding()
    }

    update_current_finding() {
        // Update finding list and ensure that selected finding is in
        // visbile finding range.
        let findings = visible_findings(RESULTVIEW.current_page)
        let position_new = Math.min(findings.length - 1, RESULTVIEW.error_selected)
        position_new = Math.max(0, position_new)
        findingbox.update_findings(position_new)
    }

    update_finding(findingid, status) {
        let url = `${API}/documents/${SERVICE.documentid}/findings/${findingid}`
        $.ajax({
            type: 'PUT',
            url: url,
            data: { 'status': status },
            error: function (request, textStatus, error) {
                // TODO: ADD ERROR HANDLER
            },
            success: function (response) {
                SERVICE.finding_update(findingid, status)
                navigator.update_page_navigator()
            }
        });
    }
}

const show_page = function (pagenumber) {
    // Open selected `page` and update findings.
    if (SERVICE.empty || empty(pagenumber)) {
        return
    }
    RESULTVIEW.reset_finding_selector(pagenumber)
    let selected = page(pagenumber)
    if (selected.content == null) {
        SERVICE.update_pagecontent(pagenumber, function () {
            show_page(pagenumber)
        })
        return
    }
    RESULTVIEW.hide_all()
    if (pagenumber < 0 || pagenumber >= FIRST_SPECIAL) {
        open_special(pagenumber)
    } else {
        if (MODERN) {
            show_pdfpage(pagenumber)
        } else {
            show_pngpage(pagenumber)
        }
    }
    navigator.highlight_pagenumber(pagenumber)
    findingbox.update_findings()
    navigator.shorten_pagenumers()
}

const show_pngpage = function (pagenumber) {
    if (pagenumber < 0) {
        return
    }
    let source = pdfpage_source(pagenumber)
    let html = `
    <style>
        #show_page {
            background: url("${source}");
            background-repeat: round;
        }
    </style>
    <img id="show_page" src="${source}" style="width:100%;">
    `
    $('#error_page_content').html(html)
    $('#pdfview_content').show()
}

const show_pdfpage = function (pagenumber) {
    if (SERVICE.pdf == null) {
        return
    }
    pagenumber = pagenumber + 1
    SERVICE.pdf.getPage(pagenumber).then(function (page) {
        let scale = 5.0;
        let viewport = page.getViewport({ scale: scale, });

        let canvas = $('#error_page_content')[0]
        let context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        let renderContext = {
            canvasContext: context,
            viewport: viewport,
        };
        page.render(renderContext);
    });
    $('#pdfview_content').show()
}

const open_special = function (pagenumber) {
    let selected = page(pagenumber)
    RESULTVIEW.hide_all()
    // TODO: REMOVE LATER
    if (selected.page == 1024 || selected.page == OVERVIEW) {
        RESULTVIEW.show_overview()
    } else if (selected.page == FOOTNOTES) {
        RESULTVIEW.show_footnotes()
    } else if (selected.page == CAPTIONS) {
        RESULTVIEW.show_captions()
    } else if (selected.page == HYPERLINKS) {
        RESULTVIEW.show_hyperlinks()
    } else if (selected.page == DOCSTYLE) {
        RESULTVIEW.show_docstyle()
    } else if (selected.page == BIBLIOGRAPHY) {
        RESULTVIEW.show_bibliography()
    } else if (selected.page == PROPERTIES) {
        RESULTVIEW.show_pdf_properties()
    } else if (selected.page == FINDINGS) {
        RESULTVIEW.show_findings()
    } else if (selected.page == SCORE) {
        $('#error_page_content').html(selected.content)
        $('#pdfview_content').show()
    } else if (selected.page == CHECKLIST) {
        RESULTVIEW.show_checklist()
    }
}

const pdfpage_source = function (pagenumber) {
    let documentid = SERVICE.documentid
    let png = `${pagenumber}.png`
    if (png.length == 5) {
        png = '00' + png
    } else if (png.length == 6) {
        png = '0' + png
    }
    let source = `${documentid}/${png}`
    return source
}


const RESULTVIEW = new ResultView()
