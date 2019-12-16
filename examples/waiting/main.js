
function make_ready(item) {
    item.classList.remove("inprogress")
    item.classList.add("done")
    item.innerHTML = '<img src="smiley.bmp" style="border-radius: 3px;">'
    // item.innerHTML = ""

}
function make_running(item) {
    item.classList.remove("todo")
    item.classList.add("inprogress")
    item.innerHTML = '<img src="loader.gif" style="border-radius: 3px;">'
}
function make_error(item) {
    item.classList.remove("inprogress")
    item.classList.add("failed")
    item.innerHTML = '<img src="frowny.bmp" style="border-radius: 3px;">'
}

function enable_fastview(processid) {
    fastview = document.getElementById("fastview")
    fastview.href = "fastview.html"

    result = document.getElementById("resultview")
    result.href = "result.html"
}


function update(status) {
    for (let stateid = 0; stateid < status.length; stateid++) {
        let item = status[stateid]
        statusitem = document.getElementById("status_" + stateid)
        if (item == 0) {
            make_ready(statusitem)
        }
        if (item == 1) {
            make_running(statusitem)
        }
        if (item >= 2) {
            make_error(statusitem)
        }
    }
}

function onload() {
    setTimeout(() => update([1, -1, -1, -1, -1, -1]), 0);

    setTimeout(() => update([0, 1, -1, -1, -1, -1]), 1000);

    setTimeout(() => update([0, 0, 1, -1, -1, -1]), 2000);
    setTimeout(() => update([0, 0, 1, 1, -1, -1]), 3000);
    setTimeout(() => enable_fastview(1337), 3000);
    setTimeout(() => enable_fastview(1337), 3000);
    setTimeout(() => update([0, 0, 1, 1, 1, -1]), 3000);
    setTimeout(() => update([0, 0, 0, 1, 1, -1]), 3000);
    setTimeout(() => update([0, 0, 0, 0, 0, 1]), 5000);
    setTimeout(() => update([0, 0, 0, 0, 0, 2]), 7000);
}
