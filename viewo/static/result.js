"use strict";

/** Result View

    Navigator
    ShowHide/Selector

*/

class ResultView {

    init() {
        this.error_page = null
        this.error_selected = null
        this.content = []
    }

    update_content(content) {
        this.content = content
        navigator.update_page_navigator()
        this.show_page(0)
    }

    show_page(page) {
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
        return this.error_selected
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

    loop(process) {
        // TODO: MOVE TO SEPARATE DATA MANAGER?
        let ajax = new XMLHttpRequest()
        ajax.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let downloaded = this.responseText
                downloaded = JSON.parse(downloaded)
                result_view.update_content(downloaded.content)
                if (downloaded.status == 1) {
                    // process is currently running
                    setTimeout(() => loop(process), 3000);
                }
            }
        }
        ajax.open("GET", `/waiting/resultview/status/${process}`, true)
        ajax.send()
    }
}

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
    }

    show_finding(id) {
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
        this.update_finding_text()
    }

    next_finding() {
        //Iterate error message headline box downwards
        let next_id = this.result.current_finding + 1
        if (next_id < this.result.findings.length) {
            this.show_finding(next_id)
        } else {
            this.show_finding(0)
        }
    }

    previous_finding() {
        //Iterate error message headline box upwards
        let next_id = this.result.current_finding - 1
        if (next_id >= 0) {
            this.show_finding(next_id)
        } else {
            this.show_finding(this.result.findings.length - 1)
        }
    }

    update_findings() {
        /**
         * Update list of selectable findings of current page. If no
         * finding is detected for current page, finding box will be
         * disabled.
         */
        let error_page_selector = $('#error_list')[0]
        // TODO: CHECK FOR BETTER REMOVEMENT
        error_page_selector.innerHTML = ''
        for (let index in this.result.findings) {
            let item = this.result.findings[index]
            add_li_selector(error_page_selector, index, item.title, item.number)
        }
        this.result.error_selected = 0
        let mark = $('#error_selected_0')
        if (mark.length > 0) {
            mark[0].classList.add('highlighted')
            this.update_finding_text()
        }
        this.show_finding(this.result.error_selected)

        if (this.result.findings.length == 0) {
            // disable error bar if no error is provided
            $('#error')[0].classList.add('hidden')
        } else {
            $('#error')[0].classList.remove('hidden')
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

    toggle_finding(finding) {
        $('#finding_' + finding).toggle()
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
        let error_page_list = $('#error_page_selector_list')[0]
        // TODO: CHECK FOR BETTER REMOVEMENT
        error_page_list.innerHTML = ''
        for (let id in this.result.content) {
            if (this.error_pages_only) {
                // skip pages which contains no error
                let no_findings = result_view.content[id].findings.length == 0
                if (no_findings) {
                    continue
                }
            }
            let item = result_view.content[id].page + 1
            add_li_button(error_page_list, id, item)
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

const result_view = new ResultView()
const navigator = new Navigator(result_view)
const findingbox = new FindingBox(result_view)

function show(id) {
    // TODO: REMOVE LATER
    findingbox.show_finding(id)
}

function add_li_button(parent, page, text) {
    let button = document.createElement('button')
    button.setAttribute('type', 'button')
    button.setAttribute('onclick', `javascript:result_view.show_page(${page})`)
    button.innerText = text
    let node = document.createElement('li')
    node.appendChild(button)
    parent.appendChild(node)
}

function add_li_selector(parent, page, text, number) {
    let node = document.createElement('li')
    node.setAttribute('id', `error_selected_${page}`)
    node.setAttribute('onclick', `javascript:show(${page})`)
    let selector = '<input id="error_selector_checkbox_' + page + '"'
        + ' type="checkbox" checked="true" ' +
        'onclick="javascript:show_hide(' + number + ')">'
    node.innerHTML = selector + text
    parent.appendChild(node)
}

function show_hide(number) {
    //REMOVE LATER
    findingbox.toggle_finding(number)
}

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
    })
}
