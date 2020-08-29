var file_upload_view = {

    init: function () {
        $("input[value='url']").on('click', function () {
            file_upload_view.open_url()
        });
        $("input[value='local']").on('click', function () {
            file_upload_view.open_file()
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
}

$(document).ready(function () {
    file_upload_view.init()
})
