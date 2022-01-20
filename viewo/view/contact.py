# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import flask_wtf
import wtforms

contact_ = flask.Blueprint('contact', __name__)  # pylint:disable=C0103


@contact_.route('/contact', methods=['GET'])
def contact():
    form = ContactForm()
    return flask.render_template(
        'public/contact/contact.html',
        form=form,
    )


MESSAGE_ERROR = ('Nachricht konnte nicht übermittelt werden. '
                 'Verwenden Sie stattdessen den E-Mail-Kontakt.')


@contact_.route('/contact', methods=['POST'])
def message_send():
    title = flask.request.form.get('title', None)
    email = flask.request.form.get('email', None)
    message = flask.request.form.get('message', None)
    if not all((title, email, message)):
        flask.flash(MESSAGE_ERROR, category='error')
        return flask.redirect(flask.url_for('contact.contact'))
    # TODO: SEND THIS DATA AS EMAIL TO OWN SERVICE ADDRESS
    return flask.render_template('public/contact/recieved.html')


class ContactForm(flask_wtf.FlaskForm):

    def __init__(self):
        super().__init__()
        priv = flask.url_for('legal.privacy')
        lega = flask.url_for('legal.agb')
        self.privacy.label.text = (
            f'Ich habe die <a href="{priv}">Datenschutzerklärung</a> '
            f'und die <a href="{lega}">allgemeinen Geschäftsbedingungen</a> '
            'gelesen und akzeptiert.')

    title = wtforms.StringField(
        'Betreff',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=8, max=256),
        ],
    )
    email = wtforms.StringField(
        'E-Mail:',
        validators=[
            # TODO: ENABLE AFTER INSTALLING email-validator
            wtforms.validators.DataRequired(),
            # wtforms.validators.Email(),
            wtforms.validators.Length(min=8, max=256),
        ],
    )
    message = wtforms.TextAreaField(
        'Nachricht:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=64, max=4048),
        ],
    )
    privacy = wtforms.BooleanField(validators=[
        wtforms.validators.DataRequired(),
    ])
    submit = wtforms.SubmitField('Absenden')
