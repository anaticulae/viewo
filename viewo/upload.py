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
from random import randint

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

from viewo.config import todo
from viewo.job import FILE_NAME
from viewo.job import JobInfo
from viewo.job import dump
from viewo.utils import today

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
        create_todo(file)
        # file.save(join(current_app.config['TODO'], filename))
        return redirect('/documents?uploaded=%s' % filename)

    return redirect('/documents')


@upload_.route('/upload/failure')
def upload_failure():
    return render_template('upload/no_file.html')


def todo_count() -> int:
    """Count folder in common `todo` folder"""
    path = todo()
    dirs = [item for item in listdir(path) if isdir(join(path, item))]
    return len(dirs)


def random_foldername():
    """Random foldername which is 10 chars long"""
    name = randint(10**(FOLDER_LENGTH - 1), 10**FOLDER_LENGTH - 1)
    return '%d' % name


def free_todo():
    """Generate file name which does not exists"""
    path = todo()
    name = random_foldername()
    while exists(join(path, name)):
        name = random_foldername()
    return name


def create_todo(file):
    """Create working folder, add info.yaml and write `file` to todo dir"""
    name = free_todo()
    todo_path = todo()

    path = join(todo_path, name)
    assert not exists(path)

    makedirs(path)
    file_path = join(path, name)
    info_path = join(path, FILE_NAME)
    # Copy provied file to todo location
    file.save(file_path)

    filename = secure_filename(file.filename)
    # Create job information
    job = JobInfo(title=filename, date=today(), index=name)
    dump(info_path, job)
