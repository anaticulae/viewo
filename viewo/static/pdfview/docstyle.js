class PDFViewDocStyle {
    constructor(result) {
        this.result = result
    }

    init_listener() {

    }

    show() {
        $('#pdfview_docstyle').show()
    }

    update(style) {
        // docstyle_fondocstyle
        $('#docstyle_text_family').text(ct(style.text_family))
        $('#docstyle_text_size').text(pt(style.text_size))
        $('#docstyle_text_distance').text(cm(style.text_distance))

        // headlines
        $('#docstyle_h1_family').text(ct(style.h1_family))
        $('#docstyle_h1_size').text(pt(style.h1_size))
        $('#docstyle_h1_before').text(pt(style.h1_before))
        $('#docstyle_h1_after').text(pt(style.h1_after))

        $('#docstyle_h2_family').text(ct(style.h2_family))
        $('#docstyle_h2_size').text(pt(style.h2_size))
        $('#docstyle_h2_before').text(pt(style.h2_before))
        $('#docstyle_h2_after').text(pt(style.h2_after))

        $('#docstyle_h3_family').text(ct(style.h3_family))
        $('#docstyle_h3_size').text(pt(style.h3_size))
        $('#docstyle_h3_before').text(pt(style.h3_before))
        $('#docstyle_h3_after').text(pt(style.h3_after))

        // footnote
        $('#docstyle_footnote_family').text(ct(style.footnote_family))
        $('#docstyle_footnote_size').text(pt(style.footnote_size))
        $('#docstyle_footnote_distance').text(cm(style.footnote_distance))

        // border
        $('#docstyle_content_left').text(cm(style.content_left))
        $('#docstyle_content_right').text(cm(style.content_right))
        $('#docstyle_content_top').text(cm(style.content_top))
        $('#docstyle_content_bottom').text(cm(style.content_bottom))

        $('#docstyle_content_rotated_left').text(cm(style.content_rotated_left))
        $('#docstyle_content_rotated_right').text(cm(style.content_rotated_right))
        $('#docstyle_content_rotated_top').text(cm(style.content_rotated_top))
        $('#docstyle_content_rotated_bottom').text(cm(style.content_rotated_bottom))
    }
}

function ct(item) {
    return item != null ? `${item}` : `-`
}

function pt(item) {
    return item != null ? `${item} pt` : `-`
}

function cm(item) {
    // TODO: REMOVE THIS HACK
    return item != null ? `${Math.round(item / 25.4 * 10) / 10} cm` : `-`
}
