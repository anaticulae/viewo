"use strict";

var base = {}
const API = '/api/v0'
const TIMEOUT = 3000

base.show_done = function (content = null) {
    base.hide('#message')
    base.show('#display')
}

base.show_connecting = function (content = '') {
    if (content == '') {
        content = 'Verbindung wird hergestellt...'
    }
    base.show_message(content)
}

base.show_error = function (content = '', link = '') {
    if (content == '') {
        content = 'Dokument nicht verfügbar.'
        link = '<a href="/documents">zur Dokumentenübersicht.</a>'
    }
    let headline = 'Fehler'
    if (link != '') {
        content += `<p>${link}</p>`
    }
    base.show_message(headline, content)
}

base.show_message = function (headline, content = '') {
    base.hide('#display')
    base.show('#message')
    let message = `<h2>${headline}</h2><p>${content}</p>`
    $('#message').html(message)

}

base.hide = function (item) {
    $(item)[0].classList.add('hidden_invisible')
}

base.show = function (item) {
    $(item)[0].classList.remove('hidden')
    $(item)[0].classList.remove('hidden_invisible')
}

base.remove = function (array, index) {
    return array.slice(0, index).concat(array.slice(index + 1))
}

base.clear = function (item) {
    //TODO: REMOVE WITH SMART APPROACH
    item.html('')
}

base.scroll_to = function (item) {
    // TODO REPLACE
    let poff = $(item).position().top
    let win = $(window)
    win.scrollTop(poff)
}


base.new_image_button = function (parent = '', src = '', id = null, textid = null, link = null, alt = null, onclick = null) {
    let raw = `<button type="button" id="${id}" class="btn btn-default"`
    if (onclick != null) {
        raw += ` onclick="${onclick}" `
    }
    raw += '>'
    if (textid != null) {
        raw += `<span class="${textid}">0</span>`
    }
    raw += `<img src="/static/images/${src}" width="20" height="20" `
    if (alt != null) {
        raw += `alt="${alt}"`
    }
    raw += '/>'
    raw += '</button>'
    if (parent != '') {
        parent.append(raw)
    } else {
        return raw
    }
    // if (link != null) {
    //     $(`#${id}`).click(function () {
    //         link(this.)
    //     });
    // }
}
base.image_short = function name(src, onclick) {
    return this.new_image_button('', src, null, null, null, null, onclick)
}

const rpc = function (url, callback, error = undefined) {
    let call = `${API}${url}`
    $.ajax(call, {
        dataType: 'json',
        success: function (response) {
            callback(response)
        },
        error: function (response) {
            connection_error()
            if (error != undefined) {
                error()
            } else {
                console.log(`error: ${call}`);
            }
        }
    });
}

const rpc_post = function (url, data, callback) {
    let call = `${API}${url}`
    $.ajax(call, {
        type: 'POST',
        data: data,
        success: function (response) {
            callback(response)
        },
    }
    );
}

const rpc_raw = function (url, callback, error = undefined) {
    let call = `${API}${url}`
    $.ajax(call, {
        success: function (response) {
            callback(response)
        },
        error: function (response) {
            connection_error()
            if (error != undefined) {
                error()
            } else {
                console.log(`error: ${call}`);
            }
        }
    });
}

const user_error = function (message) {
    let entry = `<div class="alert alert-warning">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                ${message}
                </div>`
    $('#nogoodnews').append(entry)
}

const user_info = function (message) {
    let entry = `<div class="alert alert-warning">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                ${message}
                </div>`
    $('#nogoodnews').append(entry)
}

const connection_error = function () {
    user_error('Service nicht erreichbar!')
}

const fullscreen_toggle = function (component) {
    let selected = $(component)[0]
    let before = selected.classList.length
    selected.classList.remove('fullscreen')
    if (selected.classList.length == before) {
        selected.classList.add('fullscreen')
    }
}

const range = function* (start, end = null) {
    if (end == null) {
        end = start - 1
        start = 0
    }
    for (; start <= end; start++) {
        yield start;
    }
}
