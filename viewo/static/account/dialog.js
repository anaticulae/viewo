var dialog = {
    init: function (userid) {
        dialog.userid = userid
        $("#dialog_new").submit(function (event) {
            event.preventDefault();
            let title = $("input[name='title']")[0].value
            let category = $("select[name='category']")[0].value
            let text = $("textarea[name='text']")[0].value
            dialog.send_message(title, text, category)
        });
        // add empty table
        dialog.table = $('#dialog_list').DataTable({
            'data': []
        })
        // update content
        dialog.call_server()
    },

    clear: function () {
        $("input[name='title']")[0].value = ''
        $("textarea[name='text']")[0].value = ''
    },

    call_server: function () {
        $.ajax(`${API}/dialogs/${dialog.userid}`, {
            dataType: 'json',
            success: function (response) {
                dialog.update_dialogs(response.dialogs)
            },
            error: function () {
                user_error('Could not reach server.')
            }
        });
    },

    update_dialogs: function (items) {
        if (items.length == 0) {
            base.hide('#dialog_list')
        } else {
            base.show('#dialog_list')
        }
        // TODO: IMPROVE UPDATE BEHAVIOR
        dialog.table.clear()
        let data = []
        for (let item of items) {
            // convert seconds to miliseconds
            let date = moment(item['date'] * 1000).format('DD.MM.YYYY hh:mm')
            row = [
                item['title'],
                date,
                `<a href="/account/dialogs/${item['date']}">Öffnen</a>`,
            ]
            data.push(row)
        }
        dialog.table.rows.add(data);
        dialog.table.draw()
    },

    send_message: function (title, text, category) {
        let url = `${API}/dialog/add`
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'title': title,
                'text': text,
                'category': category,
            },
            timeout: TIMEOUT,
            error: function () {
                user_error('Could not reach server.')
            },
            success: function () {
                dialog.clear()
                user_info('Nachricht übermittelt.')
                dialog.call_server()
            }
        });
    }
}
