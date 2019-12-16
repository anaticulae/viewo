function make_ready(item) {
    item.classList.remove("inprogress")
    item.classList.add("done")
    // TODO: REMOVE THIS HACK
    item.innerHTML = '<img src="../static/images/emojis/smiley.bmp" style ="border-radius: 3px;" >'
}

function make_running(item) {
    item.classList.remove("todo")
    item.classList.add("inprogress")
    item.innerHTML = '<img src="../static/images/animation/loader.gif" style ="border-radius: 3px;" >'
}

function make_error(item) {
    item.classList.remove("inprogress")
    item.classList.add("failed")
    item.innerHTML = '<img src="../static/images/emojis/frowny.bmp" style ="border-radius: 3px;" >'
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

function loop(process) {
    let ajax = new XMLHttpRequest()
    ajax.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            downloaded = this.responseText
            downloaded = JSON.parse(downloaded)

            update(downloaded.states)
            if (downloaded.status == 1) {
                // process is currently running
                setTimeout(() => loop(process), 1000);
            }
        }
    }
    ajax.open("GET", 'http://localhost:5000/waiting/status/' + process, true)
    ajax.send()
}

function onload(process) {
    loop(process)
}
