var file_upload_view = {

    init: function () {
        $("#file_upload").submit(function (event) {
            event.preventDefault();
            let fd = new FormData()
            let selected = $("input[name='file']")[0].files[0]
            fd.append('file', selected)
            file_upload_view.upload_file(fd)
        });
        $("#url_upload").submit(function (event) {
            event.preventDefault();
            let url = $("input[name='url']")[0].value
            file_upload_view.upload_url(url)
        });
    },

    upload_url: function (public_url) {
        let url = `/api/v0/documents`
        $.ajax({
            type: 'POST',
            url: url,
            data: { 'url': public_url },
            error: function (response) {
                user_error(response.responseJSON['message'])
            },
            success: function (response) {
                let forward = `Falls Sie nicht weitergeleitet werden klicken Sie
                    <a href="${response['link']}">hier</a>.`
                user_error(forward)
                window.location.replace(response['link'])
            }
        });
    },

    upload_file: function (files) {
        let url = `/api/v0/documents`
        $.ajax({
            type: 'POST',
            url: url,
            data: files,
            contentType: false,
            processData: false,
            error: function (response) {
                user_error(response.responseJSON['message'])
            },
            success: function (response) {
                let forward = `Falls Sie nicht weitergeleitet werden klicken Sie
                    <a href="${response['link']}">hier</a>.`
                user_error(forward)
                window.location.replace(response['link'])
            }
        });
    }
}

function user_error(message) {
    let entry = `<div class="alert alert-warning">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                ${ message}
                </div>`
    $('#nogoodnews').append(entry)
}

$(document).ready(function () {
    file_upload_view.init()
})
