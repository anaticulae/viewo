# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask
import flask.globals
import flask_login
import link
import link.job
import werkzeug.utils

import viewo.api
import viewo.api.documents
import viewo.api.users.post
import viewo.api.users.utils.password
import viewo.api.users.utils.user
import viewo.path
import viewo.upload
import viewo.user.auth  # TODO: REFACTOR


@viewo.api.documents.api_documents.route('/documents', methods=['POST'])
def document_create() -> str:  # pylint:disable=too-many-return-statements
    if 'url' in flask.request.form:
        posturl = flask.request.form['url']
        try:
            pdf = viewo.upload.curlpdf(posturl)
        except viewo.upload.FileTooLarge:
            return viewo.api.bad('file too large')
        except viewo.upload.InvalidResource:
            return viewo.api.bad('require pdf file')
        except viewo.upload.InvalidUrl:
            return viewo.api.bad('invalid url')
        filename = 'cloud.pdf'
    else:
        if not flask.request.files:
            return viewo.api.bad('missing `file` field')
        pdf = flask.request.files['file']
        filename = werkzeug.utils.secure_filename(pdf.filename)
        if pdf.filename == '':
            # if user does not select file, browser also submit an empty part
            # without filename
            return viewo.api.bad('empty `file` field')
        if not viewo.upload.valid_pdf(pdf.stream.read(viewo.upload.HEADER_READ_SIZE)): # yapf:disable
            return viewo.api.bad('not a pdf file')
        # reset stream
        pdf.stream.seek(0)

    userid = flask_login.current_user.get_id()
    if not userid:
        # generate new random user
        userid, password = viewo.api.users.post.create_user()
        # TODO: REFACTOR
        viewo.user.auth.login_user(userid)
    else:
        password = ''
    viewo.user.auth.public_password_set(password)

    todo = link.create_todo(
        pdf,
        filename,
        todopath=viewo.path.todo(),
        owner=userid,
    )
    _, resource = os.path.split(todo)

    viewo.api.users.utils.user.user_document_append(userid, resource)

    result = viewo.api.success(
        userid=userid,
        password=password,
        document=flask.url_for(
            'api_documents.document_get',
            documentid=resource,
        ),
        link=flask.url_for('waiting.waiting_view', process=resource),
    )
    return result
