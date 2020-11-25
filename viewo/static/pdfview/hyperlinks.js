class PDFViewHyperlinks {
    constructor() {
    }

    init() {
        // add empty table
        hyperlinksview.table = $('#hyperlinks_list').DataTable({
            'data': []
        })
    }

    update_content(hyperlinks) {
        // TODO: IMPROVE UPDATE BEHAVIOR
        hyperlinksview.table.clear()
        let data = []
        for (let link of hyperlinks) {
            let row = [
                `<a href="${link.href}">${link.href.slice(0, 80)}</a>`,
                link.page,
                link.visited,
                '1',
                'X',
            ]
            data.push(row)
        }
        hyperlinksview.table.rows.add(data);
        hyperlinksview.table.draw()

    }
}

const hyperlinksview = new PDFViewHyperlinks()

$(document).ready(function () {
    hyperlinksview.init()
})
