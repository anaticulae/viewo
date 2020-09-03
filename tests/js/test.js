function test(label, body) {
    // TODO: REPLACE THIS
    body = body()
    let valid = true
    result = []
    for (let index in body) {
        if (body[index] == false) {
            valid = false
            break
        }
    }
    if (!valid) {
        console.error(`Failed: ${label}: ${body}`);
    }
}
