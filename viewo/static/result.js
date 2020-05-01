"use strict";

/** Result View

    Navigator
    ShowHide/Selector

*/

// TODO: REQUIRE DATA MANAGER

class ResultView {

    init() {
        this.document = null
        this.error_page = null
        this.error_selected = null
        this.content = []
    }

    update_content(content) {
        // INTRODUCE EVENT LISTENER CONCEPT
        this.content = content
        navigator.update_page_navigator()
        this.show_page(0)
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

        $('#error_page_content')[0].innerHTML = selected.html

        findingbox.update_findings()
        navigator.highlight_pagenumber(page)
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
            if (item.status <= SELECTED) {
                result.push(item)
            }
        }
        // let result = this.content[this.current_page].findings
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
        let findings = this.content[this.current_page].findings
        // let findings = this.findings
        if (this.current_finding < findings.length) {
            return findings[this.current_finding]
        }
        return null
    }

    get get_next_finding() {
        let findings = this.content[this.current_page].findings
        for (let index = this.current_finding; index < findings.length; index++) {
            if (findings[index].status <= SELECTED) {
                return index
            }
        }
        return null
    }

    get get_prev_finding() {
        let findings = this.content[this.current_page].findings
        for (let index = this.current_finding - 1; index >= 0; index--) {
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
        let url = `/result/${this.document}/update/finding/${findingid}/${status}`
        fetch(url, { method: "POST" }).then(resp => {
            if (status > SELECTED) {
                // TODO: CHANGE HTTP RETURN VALUE
                // this.remove_current_finding()
            }
        })
    }

    loop(process) {
        // this.document = Number(process) // 16 bits are to short, investigate later
        this.document = process
        // TODO: MOVE TO SEPARATE DATA MANAGER?
        let ajax = new XMLHttpRequest()
        ajax.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let downloaded = this.responseText
                try {
                    downloaded = JSON.parse(downloaded)
                } catch (error) {
                    base.show_error()
                }
                result_view.update_content(downloaded.content)
                if (downloaded.status == 1) {
                    // process is currently running
                    setTimeout(() => loop(process), 3000);
                }
            }
            // else { staus ==404?
            //     base.show_error('Verbindung zum Server nicht möglich.')
            // }
        }
        ajax.open("GET", `/waiting/resultview/status/${process}`, true)
        ajax.send()
    }
}


const NOT_SELECTED = 0
const SELECTED = 1
const OPEN = [NOT_SELECTED, SELECTED]
const DONE = 2
const IGNORED = 3
const REMOVED = 4

class FindingBox {

    constructor(result) {
        this.result = result
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
        // $("#finding_select_ignore").click(function () {
        //     findingbox.current_finding_ignore()
        // });
        $("#finding_select_delete").click(function () {
            findingbox.current_finding_delete()
        });
    }

    open_finding(id) {
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
        this.update_finding_navigation()
        this.update_finding_text()
    }

    next_finding() {
        //Iterate error message headline box downwards
        let next_id = this.result.current_finding + 1
        if (next_id < this.result.findings.length) {
            this.open_finding(next_id)
        } else {
            this.open_finding(0)
        }
    }

    previous_finding() {
        //Iterate error message headline box upwards
        let next_id = this.result.current_finding - 1
        if (next_id >= 0) {
            this.open_finding(next_id)
        } else {
            this.open_finding(this.result.findings.length - 1)
        }
    }

    update_findings(current = 0) {
        /**
         * Update list of selectable findings of current page. If no
         * finding is detected for current page, finding box will be
         * disabled.
         */
        let error_page_selector = $('#error_list')
        // TODO: CHECK FOR BETTER REMOVEMENT
        error_page_selector[0].innerHTML = ''

        for (let index in this.result.findings) {
            let item = this.result.findings[index]
            let text = item.title
            let selectable = ''
            if (item.selectable == '1') {
                let status = item.status
                if (status == DONE || status == REMOVED || status == IGNORED) {
                    // done, hidden or rejected
                    continue
                }
                // add optional checkbox to disable highlighted area in
                // text view by user.
                // TODO: CHECKED SEEMS TO BE WRONG
                let checked = item.status == SELECTED ? 'checked="True"' : ''
                selectable = `<input id="error_selector_checkbox_${index}" ` +
                    `type="checkbox" ${checked}>`
                // this.open_finding(index)
                if (item.status == SELECTED) {
                    this.show_finding(item)
                }
                else {
                    this.hide_finding(item)
                }
            }
            let node_selectable = `<li id="error_selected_${index}">${selectable} ${text}</li>`
            error_page_selector.append(node_selectable)
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

    update_inbox_visibility() {
        if (this.result.findings.length == 0) {
            // disable error bar if no error is provided
            $('#error')[0].classList.add('hidden_inbounds')
        } else {
            $('#error')[0].classList.remove('hidden_inbounds')
        }

    }

    update_finding_navigation() {
        if (this.result.findings.length == 1) {
            $('#error_navigator').hide()
        }
        else {
            $('#error_navigator').show()
        }
    }

    update_finding_text() {
        let message = this.result.selected_finding
        if (message == null) {
            $('#error_message')[0].innerHTML = ''
            $('#error_message_headline')[0].innerHTML = ''
        }
        else {
            $('#error_message')[0].innerHTML = message.message
            $('#error_message_headline')[0].innerHTML = message.title
        }
    }

    show_finding(finding) {
        if (finding.location['words']) {
            let page = finding.location['page']
            for (let item of finding.location['words']) {
                let word = $(`#word${page}_${item}`)
                if (word.length) {
                    word[0].classList.add('highlighted_text')
                }
            }
        }
        else {
            $('#finding_' + finding.number).fadeIn()
        }
    }

    hide_finding(finding) {
        if (finding.location['words']) {
            let page = finding.location['page']
            for (let item of finding.location['words']) {
                let word = $(`#word${page}_${item}`)
                if (word.length) {
                    word[0].classList.remove('highlighted_text')
                }
            }
        } {
            $('#finding_' + finding.number).fadeOut()
        }
    }

    toggle_finding(finding) {
        this.open_finding(finding)
        this.toggle_selected_finding()
    }

    toggle_selected_finding() {
        if (this.result.selected_finding.status == 1) {
            this.result.update_current_finding_status(0)
            this.hide_finding(this.result.selected_finding)
        } else {
            this.result.update_current_finding_status(1)
            this.show_finding(this.result.selected_finding)
        }
    }

    current_finding_done() {
        this.result.update_current_finding_status(DONE)
        this.update_box()
    }

    current_finding_ignore() {
        this.result.update_current_finding_status(IGNORED)
        this.update_box()
    }

    current_finding_delete() {
        this.result.update_current_finding_status(REMOVED)
        this.update_box()
    }

    update_box() {
        if (this.result.selected_finding != null) {
            this.show_finding(result_view.selected_finding)
        }
        this.update_inbox_visibility()
        this.update_finding_navigation()
        this.update_finding_text()
    }

}

function count_by_finding_status(findings) {
    let done = 0
    let rejected = 0
    let open = 0
    for (let finding of findings) {
        if (finding.status <= 1) {
            open += 1
        } else if (finding.status == DONE) {
            done += 1
        } else if (finding.status > DONE) {
            rejected += 1
        }
    }
    return { 'open': open, 'done': done, 'rejected': rejected }
}

class Navigator {

    constructor(result) {
        this.result = result
        // If True, only show pages which contains an error
        this.error_pages_only = false
    }

    init_listener() {
        $("#error_page_selector_toggle").click(function () {
            navigator.toggle_pages()
        });
        $("#error_next_page").click(function () {
            navigator.next_page()
        });
        $("#error_previous_page").click(function () {
            navigator.previous_page()
        });
    }

    highlight_pagenumber(page) {
        // Highlight page number as open page in upper page selector bar.
        // Remove other potential highlights of other pages.
        // TODO: SPLIT METHOD IN CLEAR AND SET/ADD
        let error_page_list = $('#error_page_selector_list')[0]
        for (let index in error_page_list.children) {
            let child = error_page_list.children[index]
            if (index == page) {
                child.classList.add('highlighted')
            } else {
                // remove possible highlight
                if (child.classList != undefined) {// do not why this is required
                    child.classList.remove('highlighted')
                }
            }
        }
    }

    previous_page() {
        let current = this.result.current_page - 1
        if (current >= 0) {
            this.result.show_page(current)
        }
        else {
            this.result.show_page(this.result.available_pages - 1)
        }
    }

    next_page() {
        let current = this.result.current_page + 1
        if (current < this.result.available_pages) {
            this.result.show_page(current)
        } else {
            this.result.show_page(0)
        }
    }

    update_page_navigator() {
        let error_page_list = $('#error_page_selector_list')
        // TODO: CHECK FOR BETTER REMOVEMENT
        error_page_list[0].innerHTML = ''
        for (let id in this.result.content) {
            if (this.error_pages_only) {
                // skip pages which contains no error
                let no_findings = this.result.content[id].findings.length == 0
                if (no_findings) {
                    continue
                }
            }
            let text = Number(id) + 1
            let btn = `<li><button type="button" id="openpage_${id}">${text}</button></li>`
            error_page_list.append(btn)
            $(`#openpage_${id}`).click(function () {
                result_view.show_page(id)
            });
        }
    }

    toggle_pages() {
        // Switch between all page numbers of the document and the pages
        // with errors only.
        let toggle = $('#error_page_selector_toggle')[0]
        if (this.error_pages_only) {
            toggle.innerText = 'hide'
        } else {
            toggle.innerText = 'show'
        }
        this.error_pages_only = !this.error_pages_only //toggle
        this.update_page_navigator()
        this.highlight_pagenumber(this.result.error_page)
    }

}

class FindingStatusCounter {

    constructor() {

    }

    build() {
        let parent = $('#finding_status_counter')
        base.new_image_button(parent, 'result/right.png', 'show_done', 'done')
        base.new_image_button(parent, 'result/wrong.png', 'show_open', 'open')
        base.new_image_button(parent, 'result/trash.png', 'show_removed', 'rejected')
    }

    init_listener() {
        $("#show_done").click(function () {
            open_todolistview(DONE)
        });
        $("#show_removed").click(function () {
            open_todolistview(REMOVED)
        });
        $("#show_open").click(function () {
            open_todolistview(OPEN)
        });

        this.update_values()
    }

    update_values(done = 0, rejected = 0, open = 0) {
        $('#finding_status_counter .done').text(done)
        $('#finding_status_counter .open').text(open)
        $('#finding_status_counter .rejected').text(rejected)
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
            open_pdfview()
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
            `<tr>
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
            });
            $(`#${done}`).click(function () {
                result_view.update_finding(finding.number, DONE)
            });
        } else {
            $(`#${restore}`).click(function () {
                result_view.update_finding(finding.number, SELECTED)
            });
        }
    }
}

function open_todolistview(category = DONE) {
    $('#pdfview').hide()
    $('#todolistview').show()

    if (category == REMOVED) {
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
    })

    statuscounter.build()
    statuscounter.init_listener()

    todolist.init_listener()
    open_todolistview()
    todolist.update_tables()

    base.show_connecting('Öffne Dokument...')

}
