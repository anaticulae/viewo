/*
*
*/

class ResultView {

    constructor() {
        this.error_page = null
        this.error_selected = null
        this.hide_all()
    }

    show_page(pagenumber) {
        // Open selected `page` and update findings.
        if (service.empty) {
            return
        }
        if (empty(pagenumber)) {
            return
        }
        let selected = page(pagenumber)
        this.error_page = pagenumber
        this.error_selected = 0
        findingbox.paged = 0
        if (selected.content == null) {
            service.update_pagecontent(pagenumber, function () {
                resultview.show_page(pagenumber)
            })
            return
        }

        if (MODERN == false) {
            $('#error_page_content').html(selected.content)
        }

        navigator.highlight_pagenumber(pagenumber)
        findingbox.update_findings()


        // use base cause jquery introduces trouble with display: block, do
        // not refactor!
        this.hide_all()
        // TODO: REMOVE LATER
        if (selected.page == 1024 || selected.page == OVERVIEW) {
            this.show_overview()
        } else if (selected.page == FOOTNOTES) {
            this.show_footnotes()
        } else if (selected.page == CAPTIONS) {
            this.show_captions()
        } else if (selected.page == HYPERLINKS) {
            this.show_hyperlinks()
        } else if (selected.page == DOCSTYLE) {
            this.show_docstyle()
        } else if (selected.page == BIBLIOGRAPHY) {
            this.show_bibliography()
        } else if (selected.page == PROPERTIES) {
            this.show_pdf_properties()
        } else if (selected.page == FINDINGS) {
            this.show_findings()
        } else {
            if (MODERN == true) {
                this.show_pdf(selected.page)
            }
            $('#pdfview_content').show()
        }
        navigator.shorten_pagenumers()
    }

    show_pdf(pagenumber) {
        if (service.pdf == null) {
            return
        }
        pagenumber = pagenumber + 1
        service.pdf.getPage(pagenumber).then(function (page) {
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
            <div class="flex_content" id="flex_content_${solution.number}">
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
                resultview.update_finding(finding.number, REMOVED)
                $(`#flex_content_${finding.number}`).hide()
            });
            $(`#${done}`).click(function () {
                resultview.update_finding(finding.number, DONE)
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
        for (let index in footnotes) {
            let item = footnotes[index]
            let userpage = parseInt(item.page) + 1
            let status = '✔'
            if (item.error != '') {
                status = '✖'
            }
            if (current != null && current != item.page) {
                list.append('<tr><td style="border-top:solid black 1px;" colspan="4"></td></tr>')
            }
            current = item.page
            let href = `footnote_openpage${index}`
            let row = `
            <tr>
            <td class="center top">${item.number}</td>
            <td class="expand"><span id="${href}" class="click underline">${item.title}</span></td>
            <td class="center top">${userpage}</td>
            <td class="center top">${status}</td>
            </tr>`
            list.append(row)
            $(`#${href}`).click(function () {
                $(`#openpage${item.page}`).click()
            });
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
                let userpage = Number(page.page) + 1
                let status = '✔'
                if (item.error != '') {
                    status = '✖'
                }
                if (current != null && current != item.page) {
                    list.append('<tr><td style="border-top:solid black 1px;" colspan="4"></td></tr>')
                }
                current = item.page
                let href = `footnote_openpage${index}`
                let row = `
            <tr>
            <td class="center top">${nr}</td>
            <td class="expand"><span id="${href}" class="click underline">${item.raw}</span></td>
            <td class="center top">${userpage}</td>
            <td class="center top">${status}</td>
            </tr>`
                list.append(row)
                $(`#${href}`).click(function () {
                    $(`#openpage${page.page}`).click()
                });
            }
            index += 1
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
        return resultview.error_page
    }

    get current_finding() {
        if (resultview.error_selected == null) {
            return null
        }
        return parseInt(resultview.error_selected)
    }

    get available_pages() {
        if (service.content == undefined) {
            return 0
        }
        return service.content.length
    }

    get findings() {
        if (service.content == undefined) {
            return []
        }
        if (service.content.length <= resultview.current_page) {
            return []
        }
        let result = []
        for (let item of service.content[resultview.current_page].findings) {
            result.push(item)
        }
        return result
    }

    get selected_finding() {
        let findings = visible_findings(resultview.current_page)
        // let findings = page(resultview.current_page).findings
        if (findings == undefined) {
            return null
        }
        if (this.current_finding < findings.length) {
            return findings[resultview.current_finding]
        }
        return null
    }

    get get_next_finding() {
        let findings = visible_findings(resultview.current_page)
        if (findings.length == 0) {
            return null
        }
        let current_plus = resultview.current_finding + 1
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
        let findings = visible_findings(resultview.current_page)
        if (findings.length == 0) {
            return null
        }
        let current_minus = resultview.current_finding - 1
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
        let findings = visible_findings(resultview.current_page)
        let position_new = Math.min(findings.length - 1, resultview.error_selected)
        position_new = Math.max(0, position_new)
        findingbox.update_findings(position_new)
    }

    update_finding(findingid, status) {
        let url = `${API}/documents/${service.documentid}/findings/${findingid}`
        $.ajax({
            type: 'PUT',
            url: url,
            data: { 'status': status },
            error: function (request, textStatus, error) {
                // TODO: ADD ERROR HANDLER
            },
            success: function (response) {
                service.finding_update(findingid, status)
                navigator.update_page_navigator()
            }
        });
    }
}

const resultview = new ResultView()
