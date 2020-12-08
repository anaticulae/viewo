class PDFViewBibliography {
    constructor() {
    }

    init() {
        // add empty table
        bibliographyview.table = $('#bibliography_list').DataTable({
            'data': []
        })
    }

    update_content(bibs) {
        // TODO: IMPROVE UPDATE BEHAVIOR
        bibliographyview.table.clear()
        let data = []
        for (let bib of bibs) {
            let row = [
                bib.title,
                'author',
                bib.year,
            ]
            data.push(row)
        }
        bibliographyview.table.rows.add(data);
        bibliographyview.table.draw()
    }
}

const bibliographyview = new PDFViewBibliography()

$(document).ready(function () {
    bibliographyview.init()
})
