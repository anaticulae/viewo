# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from link import create_todo
from werkzeug.utils import secure_filename

upload_ = Blueprint('upload', __name__)  # pylint:disable=invalid-name

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
        todo = create_todo(file, filename)
        _, process = os.path.split(todo)
        process = int(process)
        # file.save(join(current_app.config['TODO'], filename))
        return redirect(f'/waiting/{process}')
    return redirect('/documents')


@upload_.route('/upload/failure')
def upload_failure():
    return render_template('upload/no_file.html')
