class PDFViewBibliography {
    constructor() {
    }

    init() {
        // add empty table
        BIBLIOGRAPHYVIEW.table = $('#bibliography_list').DataTable({
            'data': []
        })
    }

    update_content(bibs) {
        // TODO: IMPROVE UPDATE BEHAVIOR
        BIBLIOGRAPHYVIEW.table.clear()
        let data = []
        for (let bib of bibs) {
            let row = [
                bib.title,
                authors_raw(bib.authors),
                bib.year,
            ]
            data.push(row)
        }
        BIBLIOGRAPHYVIEW.table.rows.add(data);
        BIBLIOGRAPHYVIEW.table.draw()
    }
}

const authors_raw = function (authors) {
    let result = ''
    for (let author of authors) {
        if (result != '') {
            result = `${result}; ${author.raw}`
        }
        else {
            result = author.raw
        }
    }
    return result
}

const BIBLIOGRAPHYVIEW = new PDFViewBibliography()

$(document).ready(function () {
    BIBLIOGRAPHYVIEW.init()
})
