var messages = {
    init: function (userid, dialogid) {
        messages.userid = userid
        messages.dialogid = dialogid
        $("#message_add").submit(function (event) {
            event.preventDefault();
            let text = $("textarea[name='text']")[0].value
            messages.send_message(text, messages.userid, messages.dialogid)
        });
        messages.call_server()
    },

    clear: function () {
        $("textarea[name='text']")[0].value = ''
    },

    call_server: function () {
        $.ajax(`${API}/dialog/${messages.userid}/${messages.dialogid}`, {
            dataType: 'json',
            success: function (response) {
                messages.update_messages(response.messages)
            },
            error: function () {
                user_error('Could not reach server.')
            }
        });
    },

    update_messages: function (items) {
        content = $('#messages')
        content.html('')
        for (let item of items) {
            // convert seconds to miliseconds
            let date = moment(item.date * 1000).format('DD.MM.YYYY hh:mm')
            row = ``
            if (item['title']) {
                row += `<h3>${item.title}</h3>`
            }
            if (item.writer) {
                row += `${item.writer}: ${date}<br />`
            } else {
                row += `Antwort: ${date}<br />`
            }
            // display newlines correctly
            let text = item.text.replace(/\n/g, '<br>')
            row += `<p>${text}</p><br/>`
            content.append(row)
        }
    },

    send_message: function (text, userid, parent) {
        let url = `${API}/dialog/add`
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'text': text,
                'parent': parent,
                'userid': userid,
            },
            timeout: TIMEOUT,
            error: function () {
                user_error('Could not reach server.')
            },
            success: function () {
                messages.clear()
                user_info('Nachricht übermittelt.')
                messages.call_server()
            }
        });
    }
}
