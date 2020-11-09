"use strict";

/**
    Result View

    Navigator
    ShowHide/Selector

*/

// TODO: REQUIRE DATA MANAGER

class Navigator {

    constructor(result) {
        this.result = result
        // If True, only show pages which contains an error. Start in error
        // mode to show the findings first.
        this.error_pages_only = false
        this.items = 0
    }

    init_listener() {
        $("#pdfview_navigation_toggle").click(function () {
            navigator.toggle_pages()
        });
        $("#pdfview_next_page").click(function () {
            navigator.next_page()
        });
        $("#pdfview_previous_page").click(function () {
            navigator.previous_page()
        });
    }

    highlight_pagenumber(page) {
        // Highlight page number as open page in upper page selector bar.
        // Remove other potential highlights of other pages.
        // TODO: SPLIT METHOD IN CLEAR AND SET/ADD
        let error_page_list = $('#pdfview_navigation_list')[0]
        for (let index in error_page_list.children) {
            let child = error_page_list.children[index]
            if (child.classList != undefined) {
                child.classList.remove('highlighted')
            }
        }
        // let pdfpage = this.result.pagecontent(page).page
        let current = $(`#openpage_${page}`)
        if (current.length == 1) {
            current[0].classList.add('highlighted')
        }
    }

    previous_page() {
        findingbox.paged = 0
        if (this.error_pages_only) {
            let current = this.result.current_page
            do {
                current = (current - 1 + this.result.available_pages) % this.result.available_pages
                if (current == this.result.current_page) {
                    // no page change possible, stay on page
                    return;
                }
            } while (this.result.content[current].findings.filter(s => visible(s)).length == 0)
            this.result.show_page(current)
        }
        else {
            let previous = previous_page_visible(this.result.current_page)
            this.result.show_page(previous)
        }
    }

    next_page() {
        findingbox.paged = 0
        if (this.error_pages_only) {
            let current = this.result.current_page
            do {
                current = (current + 1) % this.result.available_pages
                if (current == this.result.current_page) {
                    // no page change possible, stay on page
                    return;
                }
            } while (this.result.content[current].findings.filter(s => visible(s)).length == 0)
            this.result.show_page(current)
        } else {
            let next = next_page_visible(this.result.current_page)
            this.result.show_page(next)
        }
    }

    update_page_navigator() {
        let error_page_list = $('#pdfview_navigation_list')
        // TODO: CHECK FOR BETTER REMOVEMENT
        error_page_list.html('')
        for (let page of service.pages) {
            let btn = `<button type="button" id="openpage_${page.page}">${page.title}</button>`
            error_page_list.append(btn)
            $(`#openpage_${page.page}`).click(function () {
                resultview.show_page(page.page)
            });
            if (page.content == SPECIALCONTENT_EMPTY) {
                $(`#openpage_${page.page}`).hide()
            }
        }
    }

    /**
     * Switch between all page numbers of the document and the pages ith
     * errors only.
     */
    toggle_pages() {
        let toggle = $('#pdfview_navigation_toggle')[0]
        if (this.error_pages_only) {
            toggle.innerText = 'hide'
        } else {
            toggle.innerText = 'show'
        }
        this.error_pages_only = !this.error_pages_only //toggle
        this.update_page_navigator()
        this.set_on_valid_hidden_page()
    }

    set_on_valid_hidden_page() {
        // ensure to be on valid page after changing from selective pages
        // to all pages.
        this.next_page()
        this.previous_page()
    }

}

class FindingStatusCounter {

    constructor() {

    }

    build() {
        let parent = $('#finding_status_counter')
        base.new_image_button(parent, 'result/wrong.png', 'show_open', 'open')
        base.new_image_button(parent, 'result/right.png', 'show_done', 'done')
        base.new_image_button(parent, 'result/trash.png', 'show_removed', 'rejected')
    }

    init_listener() {
        $("#show_done").click(function () {
            open_todolistview(DONE)
        });
        $("#show_removed").click(function () {
            open_todolistview(NOT_WANTED)
        });
        $("#show_open").click(function () {
            open_todolistview(OPEN)
        });
        this.update_values()
    }

    update_values(done = 0, rejected = 0, open = 0) {
        // TODO: Improve animation, maybe slide from top down or something,
        // reduce amout of required code
        $('#finding_status_counter .done').fadeOut()
        $('#finding_status_counter .open').fadeOut()
        $('#finding_status_counter .rejected').fadeOut()

        $('#finding_status_counter .done').text(done)
        $('#finding_status_counter .open').text(open)
        $('#finding_status_counter .rejected').text(rejected)

        $('#finding_status_counter .done').fadeIn()
        $('#finding_status_counter .open').fadeIn()
        $('#finding_status_counter .rejected').fadeIn()
    }

    update() {
        let counted = count_by_finding_status(resultview.document_findings)
        this.update_values(counted.done, counted.rejected, counted.open)
    }
}

class TodoListView {

    constructor(result) {
        this.result = result
    }

    init_listener() {
        $("#todolistview_show_pdfview").click(function () {
            open_pdfview(resultview.current_page)
        });
    }

    update_tables() {
        let open = $('#todolistview_table_open')
        let done = $('#todolistview_table_done')
        let removed = $('#todolistview_table_removed')

        base.clear(open)
        base.clear(done)
        base.clear(removed)

        let findings = this.result.document_findings

        for (let finding of findings) {
            let status = finding.status
            if (status in OPEN) {
                this.create_finding_line(open, finding)
            } else if (status == DONE) {
                this.create_finding_line(done, finding)
            } else {
                this.create_finding_line(removed, finding)
            }
        }
    }

    create_finding_line(parent, finding) {
        let status = finding.status
        let action = ''
        if (status in OPEN) {
            var del = `finding_delete_${finding.number}`
            var done = `finding_done_${finding.number}`
            action =
                `<button type="button" id="${del}">
                    <img src="/static/images/result/trash.png" alt="delete" width="100%" height="100%" />
                 </button>
                 <button type="button" id="${done}">
                    <img src="/static/images/result/right.png" alt="done" width="100%" height="100%" />
                 </button>`
        } else {
            var restore = `finding_restore_${finding.number}`
            action =
                `<button type="button" id="${restore}">
                    <img src="/static/images/result/refresh.png" alt="done" width="100%" height="100%" />
                </button>`
        }
        let page = finding.location.page
        let page_user = Number(finding.location.page) + 1
        let openid = `_todolistview_open_finding_${finding.number}`
        let jump_to_page = `<a href = "#" id = "${openid}">${finding.title}</a>`
        let number = parent[0].rows.length + 1
        let raw =
            `< tr id = "${finding.number}" >
            <td class="center">${number}</td>
            <td>${jump_to_page}</td>
            <td class="center">${page_user}</td>
            <td class="center">${action}</td>
            </tr > `
        parent.append(raw)
        $(`#${openid}`).click(function () {
            open_pdfview(page)
        });
        if (status in OPEN) {
            $(`#${del}`).click(function () {
                resultview.update_finding(finding.number, REMOVED)
                $(`#${finding.number}`).hide()
            });
            $(`#${done}`).click(function () {
                resultview.update_finding(finding.number, DONE)
                $(`#${finding.number}`).hide()
            });
        } else {
            $(`#${restore}`).click(function () {
                resultview.update_finding(finding.number, SELECTED)
                $(`#${finding.number}`).hide()
            });
        }
    }
}

function open_todolistview(category = DONE) {
    $('#pdfview').hide()
    $('#todolistview').show()

    if (category == NOT_WANTED) {
        base.scroll_to('#removed')
    } else if (category == DONE) {
        base.scroll_to('#done')
    } else if (category == OPEN) {
        base.scroll_to('#open')
    }
}

function open_pdfview(page = 0) {
    $('#todolistview').hide()
    $('#pdfview').show()
    resultview.show_page(page)
}

const navigator = new Navigator(resultview)
const statuscounter = new FindingStatusCounter()
const findingbox = new FindingBox(resultview)
const todolist = new TodoListView(resultview)
const pdfview_properties = new PDFViewProperties(resultview)
const pdfview_docstyle = new PDFViewDocStyle(resultview)

function onload(process) {
    resultview.hide_all()
    service.update(process)
}

function init() {
    navigator.init_listener()
    findingbox.init_listener()

    // Navigate thrue error pages
    window.addEventListener('keydown', event => {
        // Hands up for vim :)
        // TODO: REFACTOR
        const key = event.key
        let active = document.activeElement.type
        if (active == 'text' || active == 'textarea' || active == 'password') {
            return
        }
        if (key == 'l' || key == 'ArrowRight') {
            navigator.next_page()
            event.preventDefault()
        }
        if (key == 'h' || key == 'ArrowLeft') {
            navigator.previous_page()
            event.preventDefault()
        }
        if (key == 'j' || key == 'ArrowDown') {
            findingbox.next_finding()
            event.preventDefault()
        }
        if (key == 'k' || key == 'ArrowUp') {
            findingbox.previous_finding()
            event.preventDefault()
        }
        if (key == 'Delete') {
            findingbox.current_finding_delete()
            event.preventDefault()
        }
        if (key == 'Enter') {
            findingbox.current_finding_done()
            event.preventDefault()
        }
    })

    statuscounter.build()
    statuscounter.init_listener()

    todolist.init_listener()
    todolist.update_tables()
    pdfview_properties.init_listener()
    pdfview_docstyle.init_listener()

    base.show_connecting('Öffne Dokument...')
}
