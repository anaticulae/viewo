"use strict";

/** Result View

    Navigator
    ShowHide/Selector

*/

// TODO: REQUIRE DATA MANAGER

const PAGESTEP = 15.0

class ResultView {

    constructor() {
        this.document = null
        this.error_page = null
        this.error_selected = null
        this.footnotes = []
        this.content = []
    }

    update_content(content, footnotes, properties, doctextstyle, captions) {
        // INTRODUCE EVENT LISTENER CONCEPT
        // add document style overview
        this.footnotes = footnotes
        this.properties = properties
        this.doctextstyle = doctextstyle
        this.captions = captions

        if (content[0].page == -1) {
            content[0].title = 'Übersicht'
        }
        if (this.footnotes.length > 0) {
            content.push(
                {
                    'content': this.footnotes,
                    'findings': [],
                    'page': 1025,
                    'title': 'Fußnoten',
                }
            )
        }
        if (this.captions.length > 0) {
            content.push(
                {
                    'content': this.captions,
                    'findings': [],
                    'page': 1026,
                    'title': 'Unterschriften',
                }
            )
        }
        content.push(
            {
                'content': this.doctextstyle,
                'findings': [],
                'page': 1027,
                'title': 'Darstellung',
            }
        )
        content.push(
            {
                'content': this.properties,
                'findings': [],
                'page': 1028,
                'title': 'Eigenschaften',
            }
        )
        this.content = content
        navigator.update_page_navigator()
        this.show_page(0)
        navigator.set_on_valid_hidden_page()
        base.show_done()
        statuscounter.update()
        todolist.update_tables()
    }

    show_page(page) {
        // Open selected `page` and update findings.
        if (this.content == undefined) {
            return
        }
        if (this.content == []) {
            return
        }
        let selected = this.content[page]
        if (selected == undefined) {
            return
        }
        this.error_page = page
        $('#error_page_content').html(selected.html)

        findingbox.update_findings()

        navigator.highlight_pagenumber(page)

        // use base cause jquery introduces trouble with display: block, do
        // not refactor!
        base.hide('#pdfview_content')
        $('#pdfview_overview').hide()
        $('#pdfview_docstyle').hide()
        $('#pdfview_footnotes').hide()
        $('#pdfview_properties').hide()
        $('#pdfview_captions').hide()
        // TODO: REMOVE LATER
        if (selected.page == 1024 || selected.page == -1) {
            this.show_overview()
        } else if (selected.page == 1025) {
            this.show_footnotes()
        } else if (selected.page == 1026) {
            this.show_captions()
        } else if (selected.page == 1027) {
            this.show_docstyle()
        } else if (selected.page == 1028) {
            this.show_pdf_properties()
        } else {
            base.show('#pdfview_content')
        }
    }

    show_overview() {
        $('#pdfview_overview').show()

        let overview = $('#pdfview_overview')
        overview.html('')
        for (let finding of this.findings) {
            if (visible(finding) == false) {
                continue
            }
            let del = `delete_${finding.number}`
            let done = `done_${finding.number}`
            let content = `
            <div class="flex_content" id="flex_content_${finding.number}">
                <h4>${finding.title}</h4>
                <div class="error_message">${finding.message}</div>
                <p class="error_options">
                    <button type="button" id="${del}">
                        <img src="/static/images/result/right.png" alt="done" width="100%" height="100%" />
                    </button>
                    <button type="button" id="${done}">
                        <img src="/static/images/result/trash.png" alt="delete" width="100%" height="100%" />
                    </button>
                </p>
            </div>
            `
            $('#pdfview_overview').append(content)
            $(`#${del}`).click(function () {
                result_view.update_finding(finding.number, REMOVED)
                $(`#flex_content_${finding.number}`).hide()
            });
            $(`#${done}`).click(function () {
                result_view.update_finding(finding.number, DONE)
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
        let current = null
        for (let index in this.footnotes) {
            let item = this.footnotes[index]
            let nr = Number(index) + 1
            let userpage = Number(item.page) + 1
            let status = '✔'
            if (item.error != '') {
                status = '✖'
            }
            if (current != null && current != item.page) {
                list.append('<tr><td style="border-top:solid black 1px;" colspan="4"></td></tr>')
            }
            current = item.page

            let href = `footnote_openpage_${index}`
            let row = `
            <tr>
                <td class="center top">${nr}</td>
                <td class="expand"><span id="${href}" class="click underline">${item.title}</span></td>
                <td class="center top">${userpage}</td>
                <td class="center top">${status}</td>
            </tr>`
            list.append(row)
            $(`#${href}`).click(function () {
                $(`#openpage_${item.page}`).click()
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
        let current = null
        let index = 0
        for (let page of this.captions) {
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

                let href = `footnote_openpage_${index}`
                let row = `
            <tr>
                <td class="center top">${nr}</td>
                <td class="expand"><span id="${href}" class="click underline">${item.raw}</span></td>
                <td class="center top">${userpage}</td>
                <td class="center top">${status}</td>
            </tr>`
                list.append(row)
                $(`#${href}`).click(function () {
                    $(`#openpage_${page.page}`).click()
                });
            }
            index += 1
        }
    }

    show_pdf_properties() {
        pdfview_properties.update(result_view.properties)
        pdfview_properties.show()
    }

    show_docstyle() {
        pdfview_docstyle.update(result_view.doctextstyle)
        pdfview_docstyle.show()
    }

    pagecontent(page) {
        // determine content by index and if page is out of bounds, select
        // page by page number.
        let selected = this.content[page]
        if (selected != undefined) {
            return selected
        }
        selected = this.content.filter(s => (s.page == page))
        return selected[0]
    }

    get current_page() {
        return this.error_page
    }

    get current_finding() {
        if (this.error_selected == null) {
            return null
        }
        // TODO: REMOVE THIS HACK
        return Number(this.error_selected)
    }

    get available_pages() {
        if (this.content == undefined) {
            return 0
        }
        return this.content.length
    }

    get findings() {
        if (this.content == undefined) {
            return []
        }
        if (this.content.length <= this.current_page) {
            return []
        }
        let result = []
        for (let item of this.content[this.current_page].findings) {
            result.push(item)
        }
        return result
    }

    get document_findings() {
        if (this.content == undefined) {
            return []
        }
        let result = []

        for (let items of this.content) {
            for (let item of items.findings) {
                result.push(item)
            }
        }
        return result
    }

    get selected_finding() {
        let findings = this.pagecontent(this.current_page).findings
        // let findings = this.findings
        if (this.current_finding < findings.length) {
            return findings[this.current_finding]
        }
        return null
    }

    get get_next_finding() {
        let findings = this.pagecontent(this.current_page).findings
        if (findings.length == 0) {
            return null
        }
        let current_plus = this.current_finding + 1
        if (current_plus == findings.length) {
            current_plus = 0
        }
        for (let index = current_plus; index < findings.length; index++) {
            if (visible(findings[index]) == false) {
                continue
            }
            if (findings[index].status <= SELECTED) {
                return index
            }
        }
        return null
    }

    get get_prev_finding() {
        let findings = this.pagecontent(this.current_page).findings
        if (findings.length == 0) {
            return null
        }
        let current_minus = this.current_finding - 1
        if (current_minus < 0) {
            current_minus = findings.length - 1
        }
        for (let index = current_minus; index >= 0; index--) {
            if (visible(findings[index]) == false) {
                continue
            }
            if (findings[index].status <= SELECTED) {
                return index
            }
        }
        return null
    }

    update_current_finding_status(status) {
        if (this.selected_finding == null) {
            return
        }
        let findingid = Number(this.selected_finding.number)
        this.selected_finding.status = status // remove finding

        this.update_finding(findingid, status)

        statuscounter.update()
        this.update_current_finding()
    }

    update_current_finding() {
        if (this.selected_finding.status <= SELECTED) {
            return
        }
        let next = this.get_next_finding
        if (next != null) {
            this.error_selected = next
            findingbox.update_findings(this.error_selected)
            return
        }
        let prev = this.get_prev_finding
        if (prev != null) {
            this.error_selected = prev
            findingbox.update_findings(this.error_selected)
            return
        }
        this.error_selected = null
    }

    update_finding(findingid, status) {
        let url = `/api/v0/documents/${this.document}/findings/${findingid}`
        $.ajax({
            type: 'PUT',
            url: url,
            data: { 'status': status },
            error: function (request, textStatus, error) {
                // TODO: ADD ERROR HANDLER
            }
        });
    }

    loop(process) {
        this.document = process
        $.ajax(`/waiting/resultview/status/${process}`, {
            method: "GET",
            dataType: "json",
            success: function (response) {
                result_view.update_content(
                    response.content,
                    response.footnotes,
                    response.properties,
                    response.doctextstyle,
                    response.captions,
                )
            },
            error: function () {
                // TODO: IMPROVE ERROR HANDLER
                base.show_error()
            }
        })
    }
}


class FindingBox {

    constructor(result) {
        this.result = result
        this.paged = 0
    }

    init_listener() {
        $("#finding_previous").click(function () {
            findingbox.previous_finding()
        });
        $("#finding_next").click(function () {
            findingbox.next_finding()
        });
        $("#finding_select_done").click(function () {
            findingbox.current_finding_done()
        });
        $("#finding_select_delete").click(function () {
            findingbox.current_finding_delete()
        });
    }

    open_finding(id) {
        if (id == -1) {
            // select first visible element
            for (let index in this.result.findings) {
                let item = this.result.findings[index]
                if (visible(item)) {
                    id = index
                    break
                }
            }
        }
        let old = $(`#error_selected_${this.result.error_selected}`)[0]
        let current = $(`#error_selected_${id}`)[0]

        let set_focus = $(`#error_selector_checkbox_${id}`)[0]
        if (old != null) {
            old.classList.remove("highlighted")
        }
        if (current != null) {
            current.classList.add("highlighted")
            current.focus()
        }
        if (set_focus != null) {
            set_focus.focus()
        }
        this.result.error_selected = id
        highlight_finding(this.result.selected_finding)
        this.update_finding_navigation()
        this.update_finding_text()
    }

    next_finding() {
        //Iterate error message headline box downwards
        this.open_finding(this.result.get_next_finding)
    }

    previous_finding() {
        //Iterate error message headline box upwards
        this.open_finding(this.result.get_prev_finding)
    }

    update_findings(current = -1, paged = 0) {
        /**
         * Update list of selectable findings of current page. If no
         * finding is detected for current page, finding box will be
         * disabled.
         * Using current -1 selects the first visible element
         */
        this.paged = paged
        let pdfview_navigation = $('#error_list')
        // TODO: CHECK FOR BETTER REMOVEMENT
        pdfview_navigation.html('')

        this.update_finding_pageable()

        for (let index in this.result.findings.slice(this.paged * PAGESTEP, (this.paged + 1) * PAGESTEP)) {
            index = this.paged * PAGESTEP + parseInt(index)
            let item = this.result.findings[index]
            let text = item.title
            let selectable = ''
            if (visible(item) == false) {
                // done, hidden or rejected
                hide_finding(item)
                continue
            }
            if (item.selectable == '1') {
                // add optional checkbox to disable highlighted area in
                // text view by user.
                // TODO: CHECKED SEEMS TO BE WRONG
                let checked = item.status == SELECTED ? 'checked="True"' : ''
                selectable = `<input id="error_selector_checkbox_${index}" ` +
                    `type="checkbox" ${checked}>`
                // this.open_finding(index)
                if (item.status == SELECTED) {
                    show_finding(item)
                }
                else {
                    hide_finding(item)
                }
            }
            let node_selectable = `<li id="error_selected_${index}" class="finding_button">${selectable} ${text}</li>`
            pdfview_navigation.append(node_selectable)
            $(`#error_selector_checkbox_${index}`).click(function () {
                findingbox.toggle_finding(index)
            });
            $(`#error_selected_${index}`).click(function () {
                findingbox.open_finding(index)
            });
        }
        this.result.error_selected = 0
        let mark = $('#error_selected_0')
        if (mark.length > 0) {
            mark[0].classList.add('highlighted')
            this.update_finding_text()
        }
        this.update_inbox_visibility()
        this.open_finding(current)
    }

    update_finding_pageable() {
        let pagenumbers = Math.floor((this.result.findings.length - 1) / PAGESTEP)
        if (pagenumbers == 0) {
            return
        }
        $('#error_list').append(`<li id="error_list_pageable" class="center" style="font-size:20px"></li>`)
        for (let page = 0; page <= pagenumbers; page++) {
            let label = `${page * Math.round(PAGESTEP)}`
            let link = `<a id="error_list_pageable_${page}">${label}</a>&nbsp;`
            $('#error_list_pageable').append(link)
            $(`#error_list_pageable_${page}`).click(function () {
                // findingbox.paged = page
                findingbox.update_findings(-1, page)
                $(`#error_list_pageable_${page}`)[0].classList.add('highlighted')
            });
        }
        if (this.paged == 0 && $(`#error_list_pageable_0`)[0]) {
            $(`#error_list_pageable_0`)[0].classList.add('highlighted')
        }
    }

    update_inbox_visibility() {
        if (this.result.findings.filter(s => visible(s)).length == 0) {
            // disable error bar if no error is provided
            $('#error')[0].classList.add('hidden_inbounds')
        } else {
            $('#error')[0].classList.remove('hidden_inbounds')
        }
    }

    update_finding_navigation() {
        if (this.result.findings.filter(s => visible(s)).length == 1) {
            // use base.hide cause jquery introduce display object
            base.hide('#error_navigator')
        }
        else {
            base.show('#error_navigator')
        }
    }

    update_finding_text() {
        let message = this.result.selected_finding
        if (message == null) {
            $('#error_message').html('')
            $('#error_message_headline').html('')
        }
        else {
            $('#error_message').html(message.message)
            $('#error_message_headline').html(message.title)
        }
    }

    toggle_finding(finding) {
        this.open_finding(finding)
        this.toggle_selected_finding()
    }

    toggle_selected_finding() {
        if (this.result.selected_finding.status == 1) {
            this.result.update_current_finding_status(0)
            hide_finding(this.result.selected_finding)
        } else {
            this.result.update_current_finding_status(1)
            show_finding(this.result.selected_finding)
        }
    }

    current_finding_done() {
        this.result.update_current_finding_status(DONE)
        this.update_box()
    }

    current_finding_delete() {
        this.result.update_current_finding_status(REMOVED)
        this.update_box()
    }

    update_box() {
        if (this.result.selected_finding != null) {
            show_finding(result_view.selected_finding)
        }
        this.update_inbox_visibility()
        this.update_finding_navigation()
        this.update_finding_text()
    }

}


class Navigator {

    constructor(result) {
        this.result = result
        // If True, only show pages which contains an error. Start in error
        // mode to show the findings first.
        this.error_pages_only = true
    }

    init_listener() {
        $("#pdfview_navigation_toggle").click(function () {
            navigator.toggle_pages()
        });
        $("#pdfview_next_page").click(function () {
            navigator.next_page()
        });
        $("#pdfview_previous_page").click(function () {
            navigator.previous_page()
        });
    }

    highlight_pagenumber(page) {
        // Highlight page number as open page in upper page selector bar.
        // Remove other potential highlights of other pages.
        // TODO: SPLIT METHOD IN CLEAR AND SET/ADD
        let error_page_list = $('#pdfview_navigation_list')[0]
        for (let index in error_page_list.children) {
            let child = error_page_list.children[index]
            if (child.classList != undefined) {
                child.classList.remove('highlighted')
            }
        }
        let pdfpage = this.result.pagecontent(page).page
        let current = $(`#openpage_${pdfpage}`)
        if (current.length == 1) {
            current[0].classList.add('highlighted')
        }
    }

    previous_page() {
        if (this.error_pages_only) {
            let current = this.result.current_page
            do {
                current = (current - 1 + this.result.available_pages) % this.result.available_pages
                if (current == this.result.current_page) {
                    // no page change possible, stay on page
                    return;
                }
            } while (this.result.content[current].findings.filter(s => visible(s)).length == 0)
            this.result.show_page(current)
        }
        else {
            let current = (this.result.current_page - 1 + this.result.available_pages)
            current = current % this.result.available_pages
            this.result.show_page(current)
        }
    }

    next_page() {
        if (this.error_pages_only) {
            let current = this.result.current_page
            do {
                current = (current + 1) % this.result.available_pages
                if (current == this.result.current_page) {
                    // no page change possible, stay on page
                    return;
                }
            } while (this.result.content[current].findings.filter(s => visible(s)).length == 0)
            this.result.show_page(current)
        } else {
            let current = (this.result.current_page + 1) % this.result.available_pages
            this.result.show_page(current)
        }
    }

    update_page_navigator() {
        let error_page_list = $('#pdfview_navigation_list')
        // TODO: CHECK FOR BETTER REMOVEMENT
        error_page_list.html('')
        for (let page of this.result.content) {
            if (this.error_pages_only) {
                // skip pages which contains no error
                let no_findings = page.findings.filter(s => visible(s)).length == 0
                if (no_findings) {
                    continue
                }
            }
            let id = page.page
            let title = Number(id) + 1
            if (page.hasOwnProperty('title')) {
                title = page.title
            }
            let btn = `<button type="button" id="openpage_${id}">${title}</button>`
            error_page_list.append(btn)
            $(`#openpage_${id}`).click(function () {
                let pagenumber = navigator.result.content.findIndex(s => (s == page))
                result_view.show_page(pagenumber)
            });
        }
    }

    toggle_pages() {
        /** Switch between all page numbers of the document and the pages
            with errors only. **/
        let toggle = $('#pdfview_navigation_toggle')[0]
        if (this.error_pages_only) {
            toggle.innerText = 'hide'
        } else {
            toggle.innerText = 'show'
        }
        this.error_pages_only = !this.error_pages_only //toggle
        this.update_page_navigator()
        this.set_on_valid_hidden_page()
    }

    set_on_valid_hidden_page() {
        // ensure to be on valid page after changing from selective pages
        // to all pages.
        this.next_page()
        this.previous_page()
    }

}

class FindingStatusCounter {

    constructor() {

    }

    build() {
        let parent = $('#finding_status_counter')
        base.new_image_button(parent, 'result/wrong.png', 'show_open', 'open')
        base.new_image_button(parent, 'result/right.png', 'show_done', 'done')
        base.new_image_button(parent, 'result/trash.png', 'show_removed', 'rejected')
    }

    init_listener() {
        $("#show_done").click(function () {
            open_todolistview(DONE)
        });
        $("#show_removed").click(function () {
            open_todolistview(NOT_WANTED)
        });
        $("#show_open").click(function () {
            open_todolistview(OPEN)
        });

        this.update_values()
    }

    update_values(done = 0, rejected = 0, open = 0) {
        // TODO: Improve animation, maybe slide from top down or something,
        // reduce amout of required code
        $('#finding_status_counter .done').fadeOut()
        $('#finding_status_counter .open').fadeOut()
        $('#finding_status_counter .rejected').fadeOut()

        $('#finding_status_counter .done').text(done)
        $('#finding_status_counter .open').text(open)
        $('#finding_status_counter .rejected').text(rejected)

        $('#finding_status_counter .done').fadeIn()
        $('#finding_status_counter .open').fadeIn()
        $('#finding_status_counter .rejected').fadeIn()
    }

    update() {
        let counted = count_by_finding_status(result_view.document_findings)
        this.update_values(counted.done, counted.rejected, counted.open)
    }

}

class TodoListView {

    constructor(result) {
        this.result = result
    }

    init_listener() {
        $("#todolistview_show_pdfview").click(function () {
            open_pdfview(result_view.current_page)
        });
    }

    update_tables() {
        let open = $('#todolistview_table_open')
        let done = $('#todolistview_table_done')
        let removed = $('#todolistview_table_removed')

        base.clear(open)
        base.clear(done)
        base.clear(removed)

        let findings = this.result.document_findings

        for (let finding of findings) {
            let status = finding.status
            if (status in OPEN) {
                this.create_finding_line(open, finding)
            } else if (status == DONE) {
                this.create_finding_line(done, finding)
            } else {
                this.create_finding_line(removed, finding)
            }
        }
    }

    create_finding_line(parent, finding) {
        let status = finding.status
        let action = ''
        if (status in OPEN) {
            var del = `finding_delete_${finding.number}`
            var done = `finding_done_${finding.number}`
            action =
                `<button type="button" id="${del}">
                    <img src="/static/images/result/trash.png" alt="delete" width="100%" height="100%" />
                 </button>
                 <button type="button" id="${done}">
                    <img src="/static/images/result/right.png" alt="done" width="100%" height="100%" />
                 </button>`
        } else {
            var restore = `finding_restore_${finding.number}`
            action =
                `<button type="button" id="${restore}">
                    <img src="/static/images/result/refresh.png" alt="done" width="100%" height="100%" />
                </button>`
        }
        let page = finding.location.page
        let page_user = Number(finding.location.page) + 1
        let openid = `_todolistview_open_finding_${finding.number}`
        let jump_to_page = `<a href = "#" id = "${openid}">${finding.title}</a>`
        let number = parent[0].rows.length + 1
        let raw =
            `<tr id="${finding.number}">
                <td class="center">${number}</td>
                <td>${jump_to_page}</td>
                <td class="center">${page_user}</td>
                <td class="center">${action}</td>
            </tr>`
        parent.append(raw)
        $(`#${openid} `).click(function () {
            open_pdfview(page)
        });
        if (status in OPEN) {
            $(`#${del}`).click(function () {
                result_view.update_finding(finding.number, REMOVED)
                $(`#${finding.number}`).hide()
            });
            $(`#${done}`).click(function () {
                result_view.update_finding(finding.number, DONE)
                $(`#${finding.number}`).hide()
            });
        } else {
            $(`#${restore}`).click(function () {
                result_view.update_finding(finding.number, SELECTED)
                $(`#${finding.number}`).hide()
            });
        }
    }
}

function open_todolistview(category = DONE) {
    $('#pdfview').hide()
    $('#todolistview').show()

    if (category == NOT_WANTED) {
        base.scroll_to('#removed')
    } else if (category == DONE) {
        base.scroll_to('#done')
    } else if (category == OPEN) {
        base.scroll_to('#open')
    }
}

function open_pdfview(page = 0) {
    $('#todolistview').hide()
    $('#pdfview').show()
    result_view.show_page(page)
}

const result_view = new ResultView()
const navigator = new Navigator(result_view)
const statuscounter = new FindingStatusCounter()
const findingbox = new FindingBox(result_view)
const todolist = new TodoListView(result_view)
const pdfview_properties = new PDFViewProperties(result_view)
const pdfview_docstyle = new PDFViewDocStyle(result_view)


function onload(process) {
    result_view.loop(process)
}


function init() {
    navigator.init_listener()
    findingbox.init_listener()

    // Navigate thrue error pages
    window.addEventListener('keydown', event => {
        // Hands up for vim :)
        // TODO: REFACTOR
        const key = event.key
        let active = document.activeElement.type
        if (active == 'text' || active == 'textarea' || active == 'password') {
            return
        }
        if (key == 'l' || key == 'ArrowRight') {
            navigator.next_page()
            event.preventDefault()
        }
        if (key == 'h' || key == 'ArrowLeft') {
            navigator.previous_page()
            event.preventDefault()
        }
        if (key == 'j' || key == 'ArrowDown') {
            findingbox.next_finding()
            event.preventDefault()
        }
        if (key == 'k' || key == 'ArrowUp') {
            findingbox.previous_finding()
            event.preventDefault()
        }
        if (key == 'Delete') {
            findingbox.current_finding_delete()
            event.preventDefault()
        }
        if (key == 'Enter') {
            findingbox.current_finding_done()
            event.preventDefault()
        }
    })

    statuscounter.build()
    statuscounter.init_listener()

    todolist.init_listener()
    todolist.update_tables()
    pdfview_properties.init_listener()
    pdfview_docstyle.init_listener()

    base.show_connecting('Öffne Dokument...')
}
