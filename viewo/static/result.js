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

        update_error_page_selector(page)
        navigator.highlight_pagenumber(page)

        if (selected.findings.length == 0) {
            // disable error bar if no error is provided
            $('#error')[0].classList.add('hidden')
        } else {
            $('#error')[0].classList.remove('hidden')
        }
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
}

class FindingBox {

    constructor(result) {
        this.result = result
    }

    init_listener() {
        $("#finding_previous").click(function () {
            findingbox.previous()
        });
        $("#finding_next").click(function () {
            findingbox.next()
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

    next() {
        //Iterate error message headline box downwards
        let next_id = this.result.current_finding + 1
        if (next_id < this.result.findings.length) {
            this.show_finding(next_id)
        } else {
            this.show_finding(0)
        }
    }

    previous() {
        //Iterate error message headline box upwards
        let next_id = this.result.current_finding - 1
        if (next_id >= 0) {
            this.show_finding(next_id)
        } else {
            this.show_finding(this.result.findings.length - 1)
        }
    }

    update_finding_text() {
        let message = this.result.selected_finding
        if (message == null) {
            document.getElementById('error_message').innerHTML = ''
            document.getElementById('error_message_headline').innerHTML = ''
        }
        else {
            document.getElementById('error_message').innerHTML = message.message
            document.getElementById('error_message_headline').innerHTML = message.title
        }
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

function update_error_page_selector(page) {
    let error_page_selector = document.getElementById('error_list')
    // TODO: CHECK FOR BETTER REMOVEMENT
    error_page_selector.innerHTML = ''
    let error = result_view.content[page].findings
    for (let index in error) {
        let item = error[index]
        add_li_selector(error_page_selector, index, item.title, item.number)
    }
    result_view.error_selected = 0
    let mark = document.getElementById('error_selected_0')
    if (mark != undefined) {
        document.getElementById('error_selected_0').classList.add('highlighted')
        findingbox.update_finding_text()
    }
    findingbox.show_finding(result_view.error_selected)
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
    node.setAttribute('id', 'error_selected_' + page)
    node.setAttribute('onclick', 'javascript:show(' + page + ')')
    let selector = '<input id="error_selector_checkbox_' + page + '"'
        + ' type="checkbox" checked="true" ' +
        'onclick="javascript:show_hide(' + number + ')">'
    node.innerHTML = selector + text
    parent.appendChild(node)
}

function openclose_item(selected) {
    let before = selected.classList.length
    selected.classList.remove('hidden')
    if (selected.classList.length == before) {
        selected.classList.add('hidden')
    }
    else {
        selected.classList.remove('hidden')
    }
}

function show_hide(number) {
    // show or hide finding
    let selected = document.getElementById('finding_' + number)
    if (selected == undefined) {
        return
    }
    openclose_item(selected)
}

function onload(process) {
    loop(process)
}

function update_view(content) {
    result_view.content = content
    navigator.update_page_navigator()
    result_view.show_page(0)
}

function loop(process) {
    let ajax = new XMLHttpRequest()
    ajax.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let downloaded = this.responseText
            downloaded = JSON.parse(downloaded)

            update_view(downloaded.content)
            if (downloaded.status == 1) {
                // process is currently running
                setTimeout(() => loop(process), 3000);
            }
        }
    }
    ajax.open("GET", '/waiting/resultview/status/' + process, true)
    ajax.send()
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
            findingbox.next()
            event.preventDefault()
        }
        if (key == 'k' || key == 'ArrowUp') {
            findingbox.previous()
            event.preventDefault()
        }
    })
}
