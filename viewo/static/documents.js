/*
    Document overview table
*/

function delete_document(document) {
    let action = window.confirm('Möchten Sie das Dokument wirklich löschen?')
    if (action == false) {
        return
    }
    let line = $(`#result_table_${document}`)
    line.hide()

    let url = `${API}/documents/${document}`
    $.ajax({
        type: 'DELETE',
        url: url,
    });
}

function add_password(document) {
    do {
        var password = window.prompt('Bitte geben Sie das gewünschte Passwort ein. (mindestens 8 Stellen)')
    } while (password != undefined && password.length < 8)
    if (password == undefined) {
        return
    }
    let url = `/result/${document}/password/${password}`
    fetch(url, { method: "POST" }).then(resp => { })
}

function share_document(document) {
    let url = `/result/${document}/share`
    fetch(url, { method: "GET" }).then(resp => {
        let answer = window.prompt('Link:', `http://www.checkitweg.de/${document}`)
    })
}
