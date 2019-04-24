# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir
from os import makedirs
from os.path import exists
from os.path import isdir
from os.path import join

from configo import todo
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from link import JOB_FILE_NAME
from link import JobInfo
from link import create_todo
from link import job_dump
from utila import today
from werkzeug.utils import secure_filename

upload_ = Blueprint('upload', __name__)

FOLDER_LENGTH = 10


@upload_.route('/upload', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file transmitted')
            return redirect('/upload/failure')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/upload/failure')

        filename = secure_filename(file.filename)
        create_todo(file, filename)
        # file.save(join(current_app.config['TODO'], filename))
        return redirect('/documents?uploaded=%s' % filename)

    return redirect('/documents')


@upload_.route('/upload/failure')
def upload_failure():
    return render_template('upload/no_file.html')
