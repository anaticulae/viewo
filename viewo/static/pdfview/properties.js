class PDFViewProperties {
    constructor(result) {
        this.result = result
    }

    show() {
        $('#pdfview_properties').show()
    }

    init_listener() {
        for (let trigger of ['input', 'click', 'change', 'reset']) {
            // TODO: REMOVE THIS HACK
            for (let propertie of ['title', 'author', 'subject', 'keywords']) {
                let selected = $(`#properties_${propertie}_status`)
                selected.text('✖')
                $(`#properties_${propertie}`).on(trigger, function () {
                    let green = $(`#properties_${propertie}`)[0].value.length > 0
                    if (green) {
                        selected.text('✔')
                    } else {
                        selected.text('✖')
                    }
                });
            }
        }
    }

    update(config) {
        if (config == undefined) {
            config = {
                'author': '',
                'keywords': '',
                'password': '',
                'subject': '',
                'title': '',
            }
        }
        $('#properties_author')[0].value = config.author
        $('#properties_author').click()
        $('#properties_password')[0].value = config.password
        $('#properties_password').click()
        $('#properties_subject')[0].value = config.subject
        $('#properties_subject').click()
        $('#properties_title')[0].value = config.title
        $('#properties_title').click()
        // ?TODO JOIN KEYWORDS AND DISPLAY?
        $('#properties_keywords')[0].value = config.keywords
        $('#properties_keywords').click()
    }
}
