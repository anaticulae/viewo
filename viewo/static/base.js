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
    $('#message')[0].innerHTML = message
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
