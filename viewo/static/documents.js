/*
    Document overview table
*/

const delete_document = function (document) {
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

const add_password = function (document) {
    do {
        var password = window.prompt('Bitte geben Sie das gewünschte Passwort ein. (mindestens 8 Stellen)')
    } while (password != undefined && password.length < 8)
    if (password == undefined) {
        return
    }
    let url = `/view/${document}/password/${password}`
    fetch(url, { method: "POST" }).then(resp => { })
}

const share_document = function (document) {
    let url = `/view/${document}/share`
    fetch(url, { method: "GET" }).then(resp => {
        let answer = window.prompt('Link:', `http://www.checkitweg.de/view/${document}`)
    })
}

const documents = {
    init: function (userid) {
        // add empty table
        documents.table = $('#documents').DataTable({
            'data': [],
            aLengthMenu: [100, 50, 25, 10],
            oLanguage: {
                sLengthMenu: "Zeige _MENU_",
                sProcessing: "Lade...",
                sSearch: "Suche:",
                oPaginate: {
                    sFirst: "Anfang",
                    sLast: "Ende",
                    sNext: "Weiter",
                    sPrevious: "Zurück"
                },
                sInfo: "Zeige _START_ bis _END_ von _TOTAL_ Dokumenten",
                sEmptyTable: "Kein Dokument verfügbar",
                sInfoEmpty: "Zeige 0 bis 0 von 0 Einträgen",
            }
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
                user_error('Service nicht erreichbar.')
            }
        });
    },

    update_documents: function (items) {
        // TODO: IMPROVE UPDATE BEHAVIOR
        documents.table.clear()
        let data = []
        for (let item of items) {
            let title = item.title
            let pages = item.pages
            if (pages == undefined) {
                pages = ''
            }
            let todo = ``
            let action = ``
            let mydocument = documents.userid == item.owner
            let public = documents.userid == '00000000'
            if (item.state == 0) {
                // done
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
            } else if (item.state == 1 || item.state == -1) {
                // running or waiting
                todo = '<center>-</center>'
                if (public == false) {
                    action += base.new_image_button('', 'animation/loader.gif', null, null, null, null, `window.location.assign('waiting/${item.name}')`)
                } else {
                    action += base.new_image_button('', 'animation/loader.gif', null, null, null, null, null)
                }
                if (mydocument == false) {
                    action += base.new_image_button('', 'view/share.png', null, null, null, null, `share_document('${item.name}')`)
                } else {
                    if (public == false) {
                        action += base.new_image_button('', 'view/trash.png', null, null, null, null, `delete_document('${item.name}')`)
                    }
                }
            } else if (item.state == 2) {
                // failed
                if (public == false) {
                    action += base.new_image_button('', 'view/trash.png', null, null, null, null, `delete_document('${item.name}')`)
                }
                title = `<span style="color:red;">${title} (fehlgeschlagen)</span>`
            }
            if (item.state == -1) {
                // waiting
                title = `${title} (Warteschlange)`
            }
            let row = [
                title,
                item.date,
                pages,
                todo,
                action,
            ]
            data.push(row)
        }
        documents.table.rows.add(data);
        documents.table.draw()
    },
}
