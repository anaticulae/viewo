var documents_compare = {

    init: function () {
        $('#documents_compare_current_list').on('change', function () {
            documents_compare.update_selected()
        })
        $('#documents_compare_partner_list').on('change', function () {
            documents_compare.update_selected()
        })
        // hide error
        documents_compare.show_error('')
        // update documents selector
        documents_compare.update_documents_list()
    },

    update_documents_list: function () {
        $.ajax(`${API}/documents?done=True`, {
            dataType: 'json',
            success: function (response) {
                let docs = response['documents']
                let current_list = $('#documents_compare_current_list')
                let partner_list = $('#documents_compare_partner_list')
                current_list.html('')
                partner_list.html('')
                for (let item of docs) {
                    current_list.append(`<option value="${item['name']}">${item['date']} ${item['title']}</option>`)
                    partner_list.append(`<option value="${item['name']}">${item['date']} ${item['title']}</option>`)
                }
                documents_compare.update_selected()
            },
            error: function () {
                documents_compare.show_error('Service nicht erreichbar.')
            }
        });
    },

    update_selected: function () {
        let current = $('#documents_compare_current_list')
        let partner = $('#documents_compare_partner_list')
        documents_compare.change_userinput(true)
        documents_compare.show_message('Loading...')

        let publish = $('#documents_compare_content')
        publish.html('')
        let url = `${API}/documents/${current.val()}/findings/compare/${partner.val()}?operation=diff`
        $.ajax(url, {
            dataType: 'json',
            success: function (response) {
                publish.html('')
                compared = response['compared']['compared']
                let nodata = true
                for (let page of compared) {
                    let left = ''
                    if (page['current'].length) {
                        left = '<ol>'
                        for (let item of page['current']) {
                            left += `<li>${item['solution']['title']}</li>`
                        }
                        left += '</ol>'
                    }
                    let right = ''
                    if (page['other'].length) {
                        right = '<ol>'
                        for (let item of page['other']) {
                            right += `<li>${item['solution']['title']}</li>`
                        }
                        right += '</ol>'
                    }
                    if (page['current'].length == 0 && page['other'].length == 0) {
                        continue
                    }
                    let onebased = page['page'] + 1
                    publish.append(`
                    <tr>
                        <td>${left}</td>
                        <td>${onebased}</td>
                        <td>${right}</td>
                    </tr>
                    `)
                    nodata = false
                }
                current.attr("disabled", false)
                partner.attr("disabled", false)
                if (nodata) {
                    documents_compare.show_message('Die Dokumente sind identisch.')
                } else {
                    documents_compare.show_message('')
                }
            },
            error: function () {
                documents_compare.show_error('Service nicht erreichbar.')
            }
        })
    },

    change_userinput: function (disabled) {
        let current = $('#documents_compare_current_list')
        let partner = $('#documents_compare_partner_list')
        current.attr("disabled", disabled)
        partner.attr("disabled", disabled)
    },

    show_message: function (message) {
        let current = $('#documents_compare')
        current.show()
        $('#documents_compare_no_data').html(`<p>${message}</p>`)
        let error = $('#documents_compare_error')
        error.hide()
    },

    show_error: function (message) {
        let error = $('#documents_compare_error')
        let current = $('#documents_compare')
        if (message) {
            current.hide()
            error.html(`<p>${message}</p>`)
            error.show()
        } else {
            error.hide()
            current.show()
        }
    }
}

$(document).ready(function () {
    documents_compare.init()
})
