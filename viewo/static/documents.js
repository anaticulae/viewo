/*
    Document table

*/

function delete_document(document) {
    let line = $(`#result_table_${document}`)
    line.hide()

    let url = `/result/${document}/delete`
    fetch(url, { method: "POST" }).then(resp => {
    })
}
