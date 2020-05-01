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
