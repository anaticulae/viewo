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
    for (let finding of findings) {
        if (OPEN.includes(finding.status)) {
            open += 1
        } else if (finding.status == DONE) {
            done += 1
        } else if (NOT_WANTED.includes(finding.status)) {
            rejected += 1
        }
    }
    return { 'open': open, 'done': done, 'rejected': rejected }
}

// TODO SIMPLIFY WITH VISIT PATTERN AND GENERATOR

function show_finding(finding) {
    if (finding.status != SELECTED) {
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
    } else if (finding.location['lines']) {
        let page = finding.location['page']
        for (let item of finding.location['lines']) {
            $(`span#line${page}_${item}`).each(function () {
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
    } else if (finding.location['lines']) {
        let page = finding.location['page']
        for (let item of finding.location['lines']) {
            $(`span#line${page}_${item}`).each(function () {
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
    } else if (finding.location['lines']) {
        let page = finding.location['page']

        for (let item of finding.location['lines']) {
            $(`span#line${page}_${item}`).each(function () {
                $(this).fadeOut('fast').fadeIn()
            });
        }
    }
    else {
        $(`#finding_${finding.number}`).fadeOut('fast').fadeIn()
    }
}
