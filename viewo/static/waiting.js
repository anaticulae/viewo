/** Waiting View

  The waiting view is visible while the analysis is executed.

  General:

      As the first step, the pdf is checked for beeing valid and is
      analyzeable.
      After this, the fast view computation is started. In parallel the
      general view is executed.

  States:

      There are four possible states for every step. Waiting, Started,
      Finished, Failed.
*/
var result_waiting_view = {

    update: function (processid, status) {
        for (let stateid = 0; stateid < status.length; stateid++) {
            let item = status[stateid]
            let statusitem = $(`#status_${stateid}`)[0]
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
        if (status[1] != 1) {
            // not waiting
            result_waiting_view.enable_validation_view(processid)
        }
        if (status[2] == 0) {
            // done
            result_waiting_view.enable_fastview(processid)
        }
        if (status[3] == 0) {
            // done
            result_waiting_view.enable_resultview(processid)
        }
    },

    enable_validation_view: function (processid) {
        $("#validationview")[0].href = `/waiting/validation/${processid}`
    },

    enable_fastview: function (processid) {
        $("#fastview")[0].href = `/waiting/fastview/${processid}`
    },

    enable_resultview: function (processid) {
        $("#resultview")[0].href = `/result/${processid}`
    },

    loop: function (process) {
        let ajax = new XMLHttpRequest()
        ajax.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let downloaded = this.responseText
                downloaded = JSON.parse(downloaded)

                if (downloaded.states == undefined) {
                    // TODO: VERIFY LATER
                    $("#progress_connecting").hide()
                    $("#progress_error").show()
                    return
                }
                else {
                    $("#progress_connecting").hide()
                    $("#progress").show()
                }
                result_waiting_view.update(process, downloaded.states)

                if (downloaded.status == 1) {
                    // process is currently running
                    setTimeout(() => result_waiting_view.loop(process), 3000);
                }
            }
        }
        ajax.open("GET", `/waiting/status/${process}`, true)
        ajax.send()
    },

    onload: function (process) {
        $("#progress_error").hide()
        $("#progress").hide()
        this.loop(process)
    },

}

function make_ready(item) {
    item.classList.remove("inprogress")
    item.classList.add("done")
    item.innerHTML = '<img src="/static/images/emojis/smiley.bmp" style ="border-radius: 3px;" >'
}

function make_running(item) {
    item.classList.remove("todo")
    item.classList.add("inprogress")
    item.innerHTML = '<img src="/static/images/animation/loader.gif" style ="border-radius: 3px;" >'
}

function make_error(item) {
    item.classList.remove("inprogress")
    item.classList.add("failed")
    item.innerHTML = '<img src="/static/images/emojis/frowny.bmp" style ="border-radius: 3px;" >'
}
