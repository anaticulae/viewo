"use strict";

/**
 *
 */

const NOT_SELECTED = 0
const SELECTED = 1
const OPEN = [NOT_SELECTED, SELECTED]
const REMOVED = 3
// Remove WORKAROUND FIVE LATER
const NOT_WANTED = [REMOVED, 5] // add DISAGREE,IGNORED later?
const DONE = 4
// const IGNORED = ?

function visible(item) {
    // Determine if item is visible by user or is already deleted, judged
    // or something else.
    if (item == undefined) {
        // TODO: REMOVE LATER
        return
    }
    if (item.solution != undefined) {
        item = item.solution
    }
    let status = item.status
    return OPEN.includes(status)
}

function count_by_finding_status(findings) {
    let done = 0
    let rejected = 0
    let open = 0
    for (let page of findings) {
        if (!page.findings) {
            // no findings on this page
            continue
        }
        for (let finding of page.findings) {
            let status = finding.solution.status
            if (OPEN.includes(status)) {
                open += 1
            } else if (status == DONE) {
                done += 1
            } else if (NOT_WANTED.includes(status)) {
                rejected += 1
            }
        }
    }
    return { 'open': open, 'done': done, 'rejected': rejected }
}

// TODO SIMPLIFY WITH VISIT PATTERN AND GENERATOR

function show_finding(finding) {
    if (finding.solution.status != SELECTED) {
        return
    }
    if (finding.location['words']) {
        let page = finding.location['page']
        for (let item of finding.location['words']) {
            let word = $(`#word${page}_${item}`)
            if (word.length) {
                word[0].classList.add('highlighted_text')
            }
        }
    } else if (finding.location['line'] != null) {
        let page = finding.location['page']
        let linestart = finding.location['line']
        let lineend = finding.location['line_end'] || linestart
        for (let line of range(linestart, lineend)) {
            $(`span#line${page}_${line}`).each(function () {
                $(this)[0].classList.add('highlighted_text')
            });
        }
    }
    else {
        $('#finding_' + finding.number).fadeIn()
    }
}

function hide_finding(finding) {
    if (finding.location['words']) {
        let page = finding.location['page']
        for (let item of finding.location['words']) {
            let word = $(`#word${page}_${item}`)
            if (word.length) {
                word[0].classList.remove('highlighted_text')
            }
        }
    } else if (finding.location['line'] != null) {
        let page = finding.location['page']
        let linestart = finding.location['line']
        let lineend = finding.location['line_end'] || linestart
        for (let line of range(linestart, lineend)) {
            $(`span#line${page}_${line}`).each(function () {
                $(this)[0].classList.remove('highlighted_text')
            });
        }
    }
    else {
        $(`#finding_${finding.number}`).fadeOut('fast')
    }
}

function highlight_finding(finding) {
    if (finding == null || finding.solution.status != SELECTED) {
        return
    }
    if (finding.location['words']) {
        let page = finding.location['page']
        for (let item of finding.location['words']) {
            let word = $(`#word${page}_${item}`)
            word.fadeOut('fast').fadeIn()
        }
    } else if (finding.location['line'] != null) {
        let page = finding.location['page']
        let linestart = finding.location['line']
        let lineend = finding.location['line_end'] || linestart
        for (let line of range(linestart, lineend)) {
            $(`span#line${page}_${line}`).each(function () {
                $(this).fadeOut('fast').fadeIn()
            });
        }
    }
    else {
        $(`#finding_${finding.number}`).fadeOut('fast').fadeIn()
    }
}
