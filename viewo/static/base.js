"use strict";

var base = {}

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
    $(item)[0].classList.add('hidden')
}

base.show = function (item) {
    $(item)[0].classList.remove('hidden')
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


base.new_image_button = function (parent, src, id = null, textid = null, link = null, alt = null) {
    let raw = `<button type="button" id="${id}" class="image_button" style="width:50px;">`
    if (textid != null) {
        raw += `<span class="${textid}">0</span>`
    }
    raw += `<img src="/static/images/${src}" width="14" height="14" style="padding-left:5px" `
    if (alt != null) {
        raw += `alt="${alt}"`
    }
    raw += '/>'
    raw += '</button>'
    parent.append(raw)
    // if (link != null) {
    //     $(`#${id}`).click(function () {
    //         link(this.)
    //     });
    // }
}
