"use strict";

/** Result View

    Navigator
    ShowHide/Selector

*/

class ResultView {

    init() {
        this.document = null
        this.error_page = null
        this.error_selected = null
        this.content = []
    }

    update_content(content) {
        this.content = content
        navigator.update_page_navigator()
        this.show_page(0)
        base.show_done()
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
        let result = this.content[this.current_page].findings
        return result
    }

    get selected_finding() {
        let findings = this.findings
        if (this.current_finding < this.findings.length) {
            return findings[this.current_finding]
        }
        return null
    }

    update_current_finding_status(status) {
        if (this.selected_finding == undefined) {
            return
        }
        this.selected_finding.status = status
        let document = this.document
        let findingid = Number(this.selected_finding.number)
        let url = `/result/${document}/update/finding/${findingid}/${status}`
        fetch(url, { method: "POST" }).then(resp => {
            if (status > SELECTED) {
                // TODO: CHANGE HTTP RETURN VALUE
                this.remove_current_finding()
            }
        })
    }

    remove_current_finding() {
        findingbox.hide_finding(this.selected_finding)
        let reduce = (this.findings.length - 1) == this.current_finding
        this.content[this.current_page].findings =
            base.remove(this.content[this.current_page].findings, this.current_finding)
        if (reduce) {
            this.error_selected = this.error_selected - 1
        } else {
            if (this.findings.length == 0) {
                this.error_selected = null
            }
        }
        findingbox.update_findings(this.error_selected)
    }

    loop(process) {
        this.document = Number(process)
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
        $("#finding_select_ignore").click(function () {
            findingbox.current_finding_ignore()
        });
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
        if (this.result.findings.length == 0) {
            // disable error bar if no error is provided
            $('#error')[0].classList.add('hidden_inbounds')
        } else {
            $('#error')[0].classList.remove('hidden_inbounds')
        }
        this.open_finding(current)
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
    }

    current_finding_ignore() {
        this.result.update_current_finding_status(IGNORED)
    }

    current_finding_delete() {
        this.result.update_current_finding_status(REMOVED)
    }

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
            $(`#openpage_${id} `).click(function () {
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

    init() {
        let done = base.new_image_button('result/right.png', '#show_done', 'done')
        let open = base.new_image_button('result/wrong.png', '#show_open', 'open')
        let rejected = base.new_image_button('result/trash.png', '#show_rejected', 'rejected')

        let view = done + open + rejected
        $('#finding_status_counter')[0].innerHTML = view
        this.update()
    }

    update(done = 0, rejected = 0, open = 0) {
        $('#finding_status_counter .done').text(done)
        $('#finding_status_counter .open').text(open)
        $('#finding_status_counter .rejected').text(rejected)
    }
}

const result_view = new ResultView()
const navigator = new Navigator(result_view)
const findingbox = new FindingBox(result_view)
const statuscounter = new FindingStatusCounter()

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

    statuscounter.init()
    base.show_connecting('Öffne Dokument...')
}
