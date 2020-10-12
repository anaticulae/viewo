function openclose(selector) {
    let selected = document.getElementById(selector)
    let before = selected.classList.length
    selected.classList.remove('hidden_invisible')
    if (selected.classList.length == before) {
        selected.classList.add('hidden_invisible')
    }
    else {
        selected.classList.remove('hidden_invisible')
    }
}

function openclose_item(selected) {
    let before = selected.classList.length
    selected.classList.remove('hidden_invisible')
    if (selected.classList.length == before) {
        selected.classList.add('hidden_invisible')
    }
    else {
        selected.classList.remove('hidden_invisible')
    }
}

function add_openclose_children(selected) {
    selected.onclick = (() => {
        for (let cur of selected.childNodes) {
            openclose_item(cur)
        }
    })
}

HEADLINES = {}

function update_view(data) {
    for (let item of data) {
        // Create headline only once. If exists update current state.
        if (HEADLINES[item.title] == undefined) {
            headline_row = add_title_line(item)
            content = add_content(item.content)
            HEADLINES[item.title] = (headline_row, content)
        } else {
            headline = HEADLINES[item.title][0]
            update_title_line(headline, item)
        }
    }
}

function add_title_line(item) {
    let view = document.getElementById("linter_table")
    let title = item.title
    let error = item.content.error.length
    let warning = item.content.warning.length
    let good = item.content.good.length
    let pages = item.pages

    let headline = [
        '<a href="#">' + title + '</a>',
        pages,
        good,
        warning,
        error,
        (good + warning + error),
    ]
    let headline_row = document.createElement('tr')
    for (let datum of headline) {
        td = document.createElement('td')
        td.innerHTML = datum
        td.classList.add('fastview_group_headline')
        headline_row.appendChild(td)
    }
    headline_row.onclick = (() => {
        for (cur of headline_row.nextElementSibling.childNodes) {
            openclose_item(cur)
        }
    })
    view.appendChild(headline_row)
    return headline_row
}

function add_content(item) {
    let view = document.getElementById("linter_table")

    let tr = document.createElement('tr')
    let content = document.createElement('td')
    content.setAttribute("colspan", 6)
    tr.appendChild(content)

    let ul = add_ul(content, "fastview_group")

    if (item.error.length > 0) {
        let red = add_li(ul,
            '<a href="#">Fehler</a>',
            "fastview_group_error_headline",
        )
        red.onclick = (() => {
            for (cur of red.childNodes) {
                openclose_item(cur)
            }
        })
        red = add_ol(ul, style = "fastview_group_error")
        for (let error of item.error) {
            add_li(red, error, "fastview_group_error")
        }
    }

    if (item.warning.length > 0) {
        let orange = add_li(ul,
            '<a href="#">Warnung</a>',
            "fastview_group_warning_headline",
        )
        orange.onclick = (() => {
            for (cur of orange.childNodes) {
                openclose_item(cur)
            }
        })
        orange = add_ol(ul, "fastview_group_warning")
        for (let warning of item.warning) {
            let created = add_li(orange, warning)
            created.classList.add('hidden_invisible')
        }
    }

    if (item.good.length > 0) {
        let green = add_li(ul,
            '<a href="#">Erfolg</a>',
            "fastview_group_good_headline",
        )
        green.onclick = (() => {
            for (cur of green.childNodes) {
                openclose_item(cur)
            }
        })
        green = add_ol(ul, "fastview_group_good")
        for (let good of item.good) {
            let created = add_li(green, good)
            created.classList.add('hidden_invisible')
        }
    }
    // hide common content
    content.classList.add('hidden_invisible')
    view.appendChild(tr)
    return content
}

function update_title_line(headline, update) {
    // TODO: NOT IMPLEMENTED
}

function add_newline() {
    let view = document.getElementById("linter_table")
    let newline = document.createElement('tr')
    let td = document.createElement('td')
    td.setAttribute("colspan", 6)
    td.innerHTML = "&nbsp;"
    newline.appendChild(td)
    view.appendChild(newline)
}

function add_li(parent, text, style) {
    let node = document.createElement('li')
    node.innerHTML = text
    if (style) {
        node.classList.add(style)
    }
    parent.appendChild(node)
    return node
}

function add_ul(parent, style) {
    let node = document.createElement('ul')
    if (style) {
        node.classList.add(style)
    }
    parent.appendChild(node)
    return node
}

function add_ol(parent, style) {
    let node = document.createElement('ol')
    if (style) {
        node.classList.add(style)
    }
    parent.appendChild(node)

    return node
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
    ajax.open("GET", '/waiting/fastview/status/' + process, true)
    ajax.send()
}

function onload(process) {
    loop(process)
}
