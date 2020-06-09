const NOT_SELECTED = 0
const SELECTED = 1
const OPEN = [NOT_SELECTED, SELECTED]
const DONE = 2
const IGNORED = 3
const REMOVED = 4

function count_by_finding_status(findings) {
    let done = 0
    let rejected = 0
    let open = 0
    for (let finding of findings) {
        if (finding.status <= 1) {
            open += 1
        } else if (finding.status == DONE) {
            done += 1
        } else if (finding.status > DONE) {
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
            let line = $(`#line${page}_${item}`)
            if (line.length) {
                line[0].classList.add('highlighted_text')
            }
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
            let line = $(`#line${page}_${item}`)
            if (line.length) {
                line[0].classList.remove('highlighted_text')
            }
        }
    }
    else {
        $('#finding_' + finding.number).fadeOut()
    }
}

function highlight_finding(finding) {
    if (finding == null || finding.status != SELECTED) {
        return
    }
    if (finding.location['words']) {
        let page = finding.location['page']
        for (let item of finding.location['words']) {
            let word = $(`#word${page}_${item}`)
            word.fadeOut()
            word.fadeIn()
        }
    } else if (finding.location['lines']) {
        let page = finding.location['page']
        for (let item of finding.location['lines']) {
            let line = $(`#line${page}_${item}`)
            line.fadeOut()
            line.fadeIn()
        }
    }
    else {
        $('#finding_' + finding.number).fadeOut()
        $('#finding_' + finding.number).fadeIn()
    }
}
