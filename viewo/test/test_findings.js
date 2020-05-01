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

test("test_count_by_finding_status", function () {
    let result = count_by_finding_status(STATUS.content[0].findings)
    let check = [
        result.open == 1,
        result.done == 0,
        result.rejected == 0
    ]
    return check
});
