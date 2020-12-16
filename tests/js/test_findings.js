"use strict";

let STATUS = {
    "status": 0,
    "content": [{
        "page": 0,
        "html": "HTML CONTENT",
        "findings": [{
            "number": 0,
            "location": { "page": 0 },
            "title": "Titelseite",
            "message": "Message",
            "status": 1,
            "selectable": 0
        }]
        ,
    }],
}

QUnit.module('findings')

QUnit.test("test_count_by_finding_status", assert => {
    let result = count_by_finding_status(STATUS.content[0].findings)
    assert.equal((result.open, result.done, result.rejected), (1, 0, 0), 'counted')
});
