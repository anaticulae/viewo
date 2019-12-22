CONTENT = [
    {
        'number': 5,
        'html': 'First line\n Second Line\nThird Line',
        'error': [
            {
                'title': 'Das Dokument is sowas von kaputt.',
                'message': 'So geht das aber gar nicht\nJeha',
            },
            {
                'title': 'Lalalala alal laal lal al',
                'message': 'So geht das aber gar nicht\nJeha',
            },
            {
                'title': '1337 1337 1337',
                'message': 'So geht das \nen\n\n\nJeha',
            },
        ],
    },
    {
        'number': 9,
        'html': 'First line\n asdasd323223Second Line\nThird Line',
        'error': [],
    },
    {
        'number': 17,
        'html': 'asdas dadds saFirst line\n asdasd323223Second Line\nThird Line',
        'error': [],
    },
]

error_page = null
error_selected = null

function show_page(page) {
    let content = CONTENT[page]
    if (content == undefined) {
        return
    }

    error_page = page
    document.getElementById('error_page_content').innerHTML = content.html

    update_error_page_selector(page)
    mark_selected_page(page)

    if (content.error.length == 0) {
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
    old = document.getElementById("error_selected_" + error_selected)
    current = document.getElementById("error_selected_" + id)

    if (old != null) {
        old.classList.remove("highlighted")
    }
    if (current != null) {
        current.classList.add("highlighted")
    }
    error_selected = id
    show_error_message(error_selected)
}

function next(max_element) {
    let next_id = error_selected + 1
    if (next_id < max_element) {
        show(next_id)
    }
}

function previous() {
    let next_id = error_selected - 1
    if (next_id >= 0) {
        show(next_id)
    }
}

function update_page_selector() {
    let error_page_list = document.getElementById('error_page_selector_list')
    // TODO: CHECK FOR BETTER REMOVEMENT
    error_page_list.innerHTML = ''
    for (let id in CONTENT) {
        let item = CONTENT[id].number
        add_li_button(error_page_list, id, item)
    }
}

function update_error_page_selector(page) {
    let error_page_selector = document.getElementById('error_list')
    // TODO: CHECK FOR BETTER REMOVEMENT
    error_page_selector.innerHTML = ''
    let error = CONTENT[page].error
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
    if (message == null || message.error.length <= selected) {
        document.getElementById('error_message').innerHTML = ''
        document.getElementById('error_message_headline').innerHTML = ''
        return
    }
    message = message.error[selected]
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
    update_content()
}

function update_content() {
    update_page_selector()
    show_page(0)
}
