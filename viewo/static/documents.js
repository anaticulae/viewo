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
    let url = `/view/${document}/password/${password}`
    fetch(url, { method: "POST" }).then(resp => { })
}

function share_document(document) {
    let url = `/view/${document}/share`
    fetch(url, { method: "GET" }).then(resp => {
        let answer = window.prompt('Link:', `http://www.checkitweg.de/view/${document}`)
    })
}

var documents = {
    init: function (userid) {
        // add empty table
        documents.table = $('#documents').DataTable({
            'data': []
        })
        documents.update_user(userid)
    },

    update_user: function (userid) {
        documents.userid = userid
        documents.call_server()
    },

    call_server: function () {
        let url = `${API}/documents`
        if (documents.userid == '00000000') {
            url += '?public=True'
        }
        $.ajax(url, {
            dataType: 'json',
            success: function (response) {
                documents.update_documents(response.documents)
            },
            error: function () {
                user_error('Could not reach server.')
            }
        });
    },

    update_documents: function (items) {
        // TODO: IMPROVE UPDATE BEHAVIOR
        documents.table.clear()
        let data = []
        for (let item of items) {
            let title = item.title
            let todo = ``
            let action = ``
            let mydocument = documents.userid == item.owner
            let public = documents.userid == '00000000'
            if (item.done) {
                title = `<a href="view/${item.name}">${title}</a>`
                let closed = item.result.closed + item.result.excluded
                let findingcount = closed + item.result.open
                todo = `${closed}/${findingcount}`

                if (mydocument && public == false) {
                    // TODO: IMPROVE CODE STYLE
                    action += base.new_image_button('', 'view/lock.png', null, null, null, null, `add_password('${item.name}')`)
                    action += base.new_image_button('', 'view/share.png', null, null, null, null, `share_document('${item.name}')`)
                    action += base.new_image_button('', 'view/trash.png', null, null, null, null, `delete_document('${item.name}')`)
                } else {
                    action += base.new_image_button('', 'view/share.png', null, null, null, null, `share_document('${item.name}')`)
                }
            } else {
                todo = '<center>-</center>'
                action += base.new_image_button('', 'animation/loader.gif', null, null, null, null, `window.location.assign('waiting/${item.name}')`)
                if (mydocument == false) {
                    action += base.new_image_button('', 'view/share.png', null, null, null, null, `share_document('${item.name}')`)
                } else {
                    action += base.new_image_button('', 'view/trash.png', null, null, null, null, `delete_document('${item.name}')`)
                }
            }
            row = [
                title,
                item.date,
                todo,
                action,
            ]
            data.push(row)
        }
        documents.table.rows.add(data);
        documents.table.draw()
    },
}
