/**
 * FindingBox
 */

const PAGESTEP = 15.0

class FindingBox {

    constructor(result) {
        this.result = result
        this.paged = 0
    }

    init_listener() {
        $("#finding_previous").click(function () {
            findingbox.previous_finding()
        });
        $("#finding_next").click(function () {
            findingbox.next_finding()
        });
        $("#finding_select_done").click(function () {
            findingbox.current_finding_done()
        });
        $("#finding_select_delete").click(function () {
            findingbox.current_finding_delete()
        });
    }

    open_finding(id) {
        if (id == -1) {
            // select first visible element
            let selected = service.pagefindings(resultview.error_page)
            for (let index in selected) {
                let item = selected[index]
                if (visible(item)) {
                    id = index
                    break
                }
            }
        }
        let old = $(`#error_selected_${this.result.error_selected}`)[0]
        let current = $(`#error_selected_${id}`)[0]

        let set_focus = $(`#error_selector_checkbox_${id}`)[0]
        if (old != null) {
            old.classList.remove("highlighted")
        }
        if (current != null) {
            current.classList.add("highlighted")
            current.focus()
        }
        if (set_focus != null) {
            set_focus.focus()
        }
        this.result.error_selected = id
        highlight_finding(this.result.selected_finding)
        this.update_finding_navigation()
        this.update_finding_text()
    }

    next_finding() {
        //Iterate error message headline box downwards
        this.open_finding(this.result.get_next_finding)
    }

    previous_finding() {
        //Iterate error message headline box upwards
        this.open_finding(this.result.get_prev_finding)
    }

    update_findings(current = -1, paged = 0) {
        /**
         * Update list of selectable findings of current page. If no
         * finding is detected for current page, finding box will be
         * disabled.
         * Using current -1 selects the first visible element
         */
        this.paged = paged
        let pdfview_navigation = $('#error_list')
        // TODO: CHECK FOR BETTER REMOVEMENT
        pdfview_navigation.html('')

        this.update_finding_pageable()

        let pagefindings = visible_findings(resultview.error_page)
        for (let index in pagefindings.slice(this.paged * PAGESTEP, (this.paged + 1) * PAGESTEP)) {
            let index_paged = index
            index = this.paged * PAGESTEP + parseInt(index)
            let finding = pagefindings[index]
            let text = finding.solution.title
            let selectable = ''
            if (visible(finding) == false) {
                // done, hidden or rejected
                hide_finding(finding)
                continue
            }
            if (finding.location != undefined) {
                // add optional checkbox to disable highlighted area in
                // text view by user.
                // TODO: CHECKED SEEMS TO BE WRONG
                let checked = finding.solution.status == SELECTED ? 'checked="True"' : ''
                selectable = `<input id="error_selector_checkbox_${index_paged}" ` +
                    `type="checkbox" ${checked}>`
                // this.open_finding(index)
                if (finding.solution.status == SELECTED) {
                    show_finding(finding)
                }
                else {
                    hide_finding(finding)
                }
            }
            let node_selectable = `<li id="error_selected_${index_paged}" ` +
                `class="finding_button">${selectable} ${text}</li>`
            pdfview_navigation.append(node_selectable)
            $(`#error_selector_checkbox_${index_paged}`).click(function () {
                findingbox.toggle_finding(index)
            });
            $(`#error_selected_${index_paged}`).click(function () {
                findingbox.open_finding(index)
            })
        }
        this.result.error_selected = 0
        let mark = $('#error_selected_0')
        if (mark.length > 0) {
            mark[0].classList.add('highlighted')
            this.update_finding_text()
        }
        this.update_inbox_visibility()
        this.open_finding(current)

        // expand page-view if no findings are printed
        if (pagefindings.length == 0) {
            $('#error_page_content')[0].classList.add('expand')
        } else {
            $('#error_page_content')[0].classList.remove('expand')
        }
    }

    update_finding_pageable() {
        let pagefindings = service.pagefindings(resultview.error_page)
        let pagenumbers = Math.floor((pagefindings.length - 1) / PAGESTEP)
        if (pagenumbers <= 0) {
            return
        }
        $('#error_list').append(`<li id="error_list_pageable" class="center" style="font-size:20px"></li>`)
        for (let page = 0; page <= pagenumbers; page++) {
            let label = `${page * Math.round(PAGESTEP)}`
            let link = `<a id="error_list_pageable_${page}">${label}</a>&nbsp;`
            $('#error_list_pageable').append(link)
            $(`#error_list_pageable_${page}`).click(function () {
                // findingbox.paged = page
                findingbox.update_findings(-1, page)
                $(`#error_list_pageable_${page}`)[0].classList.add('highlighted')
            });
        }
        if (this.paged == 0 && $(`#error_list_pageable_0`)[0]) {
            $(`#error_list_pageable_0`)[0].classList.add('highlighted')
        }
    }

    update_inbox_visibility() {
        let pagefindings = service.pagefindings(resultview.error_page)
        pagefindings = pagefindings.filter(s => visible(s))
        if (pagefindings.length == 0) {
            // disable error bar if no error is provided
            $('#error')[0].classList.add('hidden_inbounds')
        } else {
            $('#error')[0].classList.remove('hidden_inbounds')
        }
    }

    update_finding_navigation() {
        let pagefindings = service.pagefindings(resultview.error_page)
        pagefindings = pagefindings.filter(s => visible(s))
        if (pagefindings.length == 1) {
            // use base.hide cause jquery introduce display object
            base.hide('#error_navigator')
        }
        else {
            base.show('#error_navigator')
        }
    }

    update_finding_text() {
        let message = this.result.selected_finding
        if (message == null) {
            $('#error_message').html('')
            $('#error_message_headline').html('')
        }
        else {
            let solution = message.solution
            $('#error_message').html(solution.description)
            $('#error_message_headline').html(solution.title)
        }
    }

    toggle_finding(finding) {
        this.open_finding(finding)
        this.toggle_selected_finding()
    }

    toggle_selected_finding() {
        if (this.result.selected_finding.solution.status == 1) {
            this.result.update_current_finding_status(0)
            hide_finding(this.result.selected_finding)
        } else {
            this.result.update_current_finding_status(1)
            show_finding(this.result.selected_finding)
        }
    }

    current_finding_done() {
        this.result.update_current_finding_status(DONE)
        this.update_box()
    }

    current_finding_delete() {
        this.result.update_current_finding_status(REMOVED)
        this.update_box()
    }

    update_box() {
        if (this.result.selected_finding != null) {
            show_finding(resultview.selected_finding)
        }
        // this.update_findings(this.current_finding)
        this.update_inbox_visibility()
        this.update_finding_navigation()
        this.update_finding_text()
    }

    get finding_max() {
        let pagefindings = visible_findings(resultview.error_page)
        let max = pagefindings.length - this.paged * PAGESTEP
        return Math.min(PAGESTEP, max)
    }

}
