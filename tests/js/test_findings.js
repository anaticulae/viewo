"use strict";

let STATUS = [
    {
        "page": 0,
        "html": "HTML CONTENT",
        "findings": [{
            "number": 0,
            "location": { "page": 0 },
            "title": "Titelseite",
            "message": "Message",
            "solution": {
                "status": 1,
            },
            "selectable": 0
        }]
    }
]

QUnit.module('findings')

QUnit.test("test_count_by_finding_status", assert => {
    let result = count_by_finding_status(STATUS)
    assert.equal((result.open, result.done, result.rejected), (1, 0, 0), 'counted')
});
