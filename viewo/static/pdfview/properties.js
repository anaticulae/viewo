class PDFViewProperties {
    constructor(result) {
        this.result = result
    }

    show() {
        $('#pdfview_properties').show()
    }

    init_listener() {
        for (let property of ['title', 'author', 'subject', 'keywords']) {
            let selected = $(`#properties_${property}_status`)
            selected.text('✖')
            $(`#properties_${property}`).on('input click change reset', function () {
                let green = $(`#properties_${property}`)[0].value.length > 0
                if (green) {
                    selected.text('✔')
                } else {
                    selected.text('✖')
                }
            });
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
                'date': {
                    'year': 2020,
                    'month': 12,
                    'day': 10,
                    'hour': 12,
                    'minute': '00',
                }
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

        $('#properties_date')[0].value = `${config.date.year}-${config.date.month}-${config.date.day}`
        $('#properties_time')[0].value = `${config.date.hour}:${config.date.minute}`
    }
}
