CONTENT = []

error_page = null
error_selected = null
// If True, only show pages which contains an error
error_pages_only = false

function show_page(page) {
    if (CONTENT == undefined) {
        return
    }
    let content = CONTENT[page]
    if (content == undefined) {
        return
    }

    error_page = page
    document.getElementById('error_page_content').innerHTML = content.html

    update_error_page_selector(page)
    mark_selected_page(page)

    if (content.findings.length == 0) {
        // disable error bar if no error is provided
        document.getElementById("error").classList.add('hidden')
    } else {
        document.getElementById("error").classList.remove('hidden')
    }
}

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

    if (old != null) {
        old.classList.remove("highlighted")
    }
    if (current != null) {
        current.classList.add("highlighted")
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
        add_li_selector(error_page_selector, index, item.title)
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
    button.setAttribute('onclick', 'javascript:show_page(' + page + ')')
    button.innerText = text
    let node = document.createElement('li')
    node.appendChild(button)
    parent.appendChild(node)
}

function add_li_selector(parent, page, text) {
    let node = document.createElement('li')
    node.setAttribute('id', 'error_selected_' + page)
    node.setAttribute('onclick', 'javascript:show(' + page + ')')
    node.innerText = text
    parent.appendChild(node)
}

function onload(process) {
    loop(process)
}

function update_view(content) {
    CONTENT = content
    update_page_selector()
    show_page(0)
}

function loop(process) {
    let ajax = new XMLHttpRequest()
    ajax.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            downloaded = this.responseText
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
        show_page(current)
    }
    else {
        show_page(CONTENT.length - 1)
    }
}

function next_page() {
    let current = error_page + 1
    let maxpages = CONTENT.length
    if (current < maxpages) {
        show_page(current)
    } else {
        show_page(0)
    }
}
