# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""View: Upload
============

NOTE: THIS IS VERY DANGEROUS CAUSE WE DOWNLOAD USER DATA TO THE SERVER
"""

import contextlib
import os
import urllib.error
import urllib.request

import flask
import link
import utila
import werkzeug.utils

upload_ = flask.Blueprint('upload', __name__)  # pylint:disable=invalid-name


@upload_.route('/upload', methods=['GET', 'POST'])
def upload_pdf():
    if flask.request.method != 'POST':
        return flask.redirect('/documents')

    file_fromurl = None
    with contextlib.suppress(KeyError):
        posturl = flask.request.form['url']
        file_fromurl = curlpdf(posturl)
        if not file_fromurl:
            return flask.redirect('/upload/failure')

    if not file_fromurl:  # POST FILE OPTION
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            flask.flash('No file transmitted')
            return flask.redirect('/upload/failure')
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flask.flash('No selected file')
            return flask.redirect('/upload/failure')
        filename = werkzeug.utils.secure_filename(file.filename)
    else:  # POST URL OPTION
        file = file_fromurl
        filename = 'fromurl.pdf'

    todo = link.create_todo(file, filename)
    _, process = os.path.split(todo)
    # file.save(join(current_app.config['TODO'], filename))
    return flask.redirect(f'/waiting/{process}')


@upload_.route('/upload/failure')
def upload_failure():
    return flask.render_template('upload/no_file.html')


MAX_FILE_SIZE = 10 * 1024 * 1024
HEADER_READ_SIZE = 1024
FILE_READ_TIMEOUT = 10
EXPECTED_PDFSTART = b'%PDF-1.'


def curlpdf(url: str):
    try:
        with urllib.request.urlopen(
                url,
                timeout=FILE_READ_TIMEOUT,
        ) as webhandle:
            header = webhandle.read(HEADER_READ_SIZE)

            # %PDF-1.5 for example
            if not header[0:len(EXPECTED_PDFSTART)] == EXPECTED_PDFSTART:
                utila.error(f'no pdf file: {url}')
                return None

            content = webhandle.read(MAX_FILE_SIZE - HEADER_READ_SIZE)
    except (ValueError, urllib.error.URLError):
        utila.error(f'invalid url: {url}')
        return None

    # TODO: ADD FILE MAX CHECK

    filecontent = header + content

    class TmpFile:

        def __init__(self, content):
            self.content = content

        def save(self, path: str):
            utila.file_replace_binary(path, self.content)

    return TmpFile(filecontent)
