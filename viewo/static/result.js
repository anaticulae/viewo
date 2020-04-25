/** Result View

*/

var result_view = {

    init: function () {
        this.error_page = null
        this.error_selected = null
        // If True, only show pages which contains an error
        this.error_pages_only = false
        this.content = []
    },

    show_page: function (page) {
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
        mark_selected_page(page)

        if (selected.findings.length == 0) {
            // disable error bar if no error is provided
            $('#error')[0].classList.add('hidden')
        } else {
            $('#error')[0].classList.remove('hidden')
        }

    }

}

CONTENT = []

error_page = null
error_selected = null
// If True, only show pages which contains an error
error_pages_only = false

function mark_selected_page(page) {
    let error_page_list = document.getElementById('error_page_selector_list')
    for (let index in error_page_list.children) {
        let child = error_page_list.children[index]
        if (index == page) {
            child.classList.add('highlighted')
        } else {
            if (child.classList != undefined) {// do not why this is required
                child.classList.remove('highlighted')
            }
        }
    }
}

function show(id) {
    let old = document.getElementById("error_selected_" + error_selected)
    let current = document.getElementById("error_selected_" + id)

    let set_focus = document.getElementById("error_selector_checkbox_" + id)
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
    error_selected = id
    show_error_message(error_selected)
}

function next() {
    let max_element = CONTENT[error_page].findings.length
    let next_id = error_selected + 1
    if (next_id < max_element) {
        show(next_id)
    } else {
        show(0)
    }
}

function previous() {
    let max_element = CONTENT[error_page].findings.length
    let next_id = error_selected - 1
    if (next_id >= 0) {
        show(next_id)
    } else {
        show(max_element - 1)
    }
}

function update_page_selector() {
    let error_page_list = document.getElementById('error_page_selector_list')
    // TODO: CHECK FOR BETTER REMOVEMENT
    error_page_list.innerHTML = ''
    for (let id in CONTENT) {
        if (error_pages_only) {
            // skip pages which contains no error
            let no_findings = CONTENT[id].findings.length == 0
            if (no_findings) {
                continue
            }
        }
        let item = CONTENT[id].page + 1
        add_li_button(error_page_list, id, item)
    }
}

function update_error_page_selector(page) {
    let error_page_selector = document.getElementById('error_list')
    // TODO: CHECK FOR BETTER REMOVEMENT
    error_page_selector.innerHTML = ''
    let error = CONTENT[page].findings
    for (let index in error) {
        let item = error[index]
        add_li_selector(error_page_selector, index, item.title, item.number)
    }
    error_selected = 0
    let mark = document.getElementById('error_selected_0')
    if (mark != undefined) {
        document.getElementById('error_selected_0').classList.add('highlighted')
        show_error_message(error_selected)
    }
    show(error_selected)
}

function show_error_message(selected) {
    let message = CONTENT[error_page]
    if (message == null || message.findings.length <= selected) {
        document.getElementById('error_message').innerHTML = ''
        document.getElementById('error_message_headline').innerHTML = ''
        return
    }
    message = message.findings[selected]
    document.getElementById('error_message').innerHTML = message.message
    document.getElementById('error_message_headline').innerHTML = message.title
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
    openclose_item(selected)
}

function onload(process) {
    loop(process)
}

function update_view(content) {
    CONTENT = content
    result_view.content = content
    update_page_selector()
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

function toggle_pages() {
    let toggle = document.getElementById('error_page_selector_toggle')
    if (error_pages_only) {
        error_pages_only = false
        toggle.innerText = 'hide'
    } else {
        error_pages_only = true
        toggle.innerText = 'show'
    }
    update_page_selector()
    mark_selected_page(error_page)
}

function previous_page() {
    let current = error_page - 1
    if (current >= 0) {
        result_view.show_page(current)
    }
    else {
        result_view.show_page(CONTENT.length - 1)
    }
}

function next_page() {
    let current = error_page + 1
    let maxpages = CONTENT.length
    if (current < maxpages) {
        result_view.show_page(current)
    } else {
        result_view.show_page(0)
    }
}

// Navigate thrue error pages
window.addEventListener('keydown', event => {
    // Hands up for vim :)
    // TODO: REFACTOR
    key = event.key
    if (key == 'l' || key == 'ArrowRight') {
        next_page()
        event.preventDefault()
    }
    if (key == 'h' || key == 'ArrowLeft') {
        previous_page()
        event.preventDefault()
    }
    if (key == 'j' || key == 'ArrowDown') {
        next()
        event.preventDefault()
    }
    if (key == 'k' || key == 'ArrowUp') {
        previous()
        event.preventDefault()
    }
})
