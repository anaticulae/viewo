class PDFViewFinding {
    constructor() {
    }

    init() {
        // add empty table
        findingview.table = $('#finding_list').DataTable({
            'data': []
        })
        // register listener
        $("#select_critical").on('click', function () {
            findingview.update_filter()
        });
        $("#select_error").on('click', function () {
            findingview.update_filter()
        });
        $("#select_improvement").on('click', function () {
            findingview.update_filter()
        });
        $("#select_closed").on('click', function () {
            findingview.update_filter()
        });
    }

    update_content(findings) {
        let dt = findingview.table
        // TODO: IMPROVE UPDATE BEHAVIOR
        dt.clear()
        let data = []
        for (let page of findings) {
            for (let finding of page.content) {
                let row = [
                    finding.solution.title,
                    page.page,
                    error_label(finding.solution.msgid),
                    status_label(finding.solution.status)
                ]
                data.push(row)
            }
        }
        dt.rows.add(data);
        findingview.update_filter()
    }

    filter_closed(closed) {
        let dt = findingview.table
        if (closed) {
            dt.column(3).search('', true).draw()
        } else {
            dt.column(3).search('offen').draw()
        }
    }

    filter_selected(error, warning, improvement) {
        let dt = findingview.table
        let filter = ['All']
        if (error) {
            filter.push('Fehler')
        }
        if (warning) {
            filter.push('Warnung')
        }
        if (improvement) {
            filter.push('Vorschlag')
        }
        filter = '\\b(' + filter.join('|') + ')\\b'
        dt.column(2).search(filter, true).draw()
    }

    update_filter() {
        let error = $("#select_critical")[0].checked
        let warning = $("#select_error")[0].checked
        let improvement = $("#select_improvement")[0].checked
        let closed = $("#select_closed")[0].checked

        findingview.filter_closed(closed)
        findingview.filter_selected(error, warning, improvement)
    }
}

const error_label = function (msgid) {
    let level = msgid[0]
    if (level == 'W') {
        return '<span class="btn btn-warning">Warnung</span>'
    }
    if (level == 'E') {
        return '<span class="btn btn-danger">Fehler</span>'
    }
    return '<span class="btn btn-success">Vorschlag</span>'
}

const status_label = function (status) {
    if (status != 1) {
        return 'geschlossen'
    }
    return 'offen'
}

const findingview = new PDFViewFinding()

$(document).ready(function () {
    findingview.init()

})
