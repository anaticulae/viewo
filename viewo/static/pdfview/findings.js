class PDFViewFinding {
    constructor() {
    }

    init() {
        // add empty table
        findingview.table = $('#finding_list').DataTable({
            'data': []
        })
    }

    update_content(findings) {
        // TODO: IMPROVE UPDATE BEHAVIOR
        findingview.table.clear()
        let data = []
        for (let page of findings) {
            for (let finding of page.content) {
                let row = [
                    finding.solution.title,
                    page.page,
                    '',
                    '',
                ]
                data.push(row)
            }
        }
        findingview.table.rows.add(data);
        findingview.table.draw()
    }
}

const findingview = new PDFViewFinding()

$(document).ready(function () {
    findingview.init()
})
