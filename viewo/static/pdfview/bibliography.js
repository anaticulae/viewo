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
                authors_raw(bib.authors),
                bib.year,
            ]
            data.push(row)
        }
        bibliographyview.table.rows.add(data);
        bibliographyview.table.draw()
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

const bibliographyview = new PDFViewBibliography()

$(document).ready(function () {
    bibliographyview.init()
})
