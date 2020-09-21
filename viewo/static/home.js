var file_upload_view = {

    init: function () {
        $("input[value='url']").on('click', function () {
            file_upload_view.open_url()
        });
        $("input[value='local']").on('click', function () {
            file_upload_view.open_file()
        });

        $("#upload").submit(function (event) {
            event.preventDefault();
            file_upload_view.upload_selected()
        });
        this.open_file()
    },

    open_url: function () {
        $("input[name='source']").parent().css("background-color", "");
        $("input[value='url']").parent().css("background-color", "gray");
        $("#file_local_view").html('')
        $("#file_url_view").html(`Webadresse: <input class="resource"
        type="text" name="url" required="required" />`)
    },

    open_file: function () {
        $("input[name='source']").parent().css("background-color", "");
        $("input[value='local']").parent().css("background-color", "gray");
        $("#file_url_view").html('')
        $("#file_local_view").html(`Lokale Datei: <input
        class="resource" type="file" name="file" required="required"/>`)
    },

    upload_selected: function () {
        let url = $("input[name='url']")[0]
        if (url == undefined) {
            let file = $("input[name='file']")[0]
            file_upload_view.upload_file(file.files)
        } else {
            url = url.value
            file_upload_view.upload_url(url)
        }
    },

    upload_url: function (public_url) {
        let url = `/api/v0/documents`
        $.ajax({
            type: 'POST',
            url: url,
            data: { 'url': public_url },
            error: function (request, textStatus, error) {
                // TODO: ADD ERROR HANDLER
            }
        });
    },

    upload_file: function (files) {
        let url = `/api/v0/documents`
        $.ajax({
            type: 'POST',
            url: url,
            data: { 'file': files },
            error: function (request, textStatus, error) {
                // TODO: ADD ERROR HANDLER
            },
            success: function (data, textStatus, request) {
                // $.reddata['link']
            }
        });
    }
}

$(document).ready(function () {
    file_upload_view.init()
})
