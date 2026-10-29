# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import utilo
import viewo_legal

legal_ = flask.Blueprint('legal', __name__)  # pylint:disable=C0103


@legal_.route('/agb', methods=['GET'])
def agb():
    return flask.render_template('public/legal/agb.html', agb=viewo_legal.agb())


@legal_.route('/impressum', methods=['GET'])
def impressum():
    return flask.render_template(
        'public/legal/impressum.html',
        impressum=viewo_legal.impressum(),
    )


@legal_.route('/privacy', methods=['GET'])
def privacy():
    return flask.render_template(
        'public/legal/privacy.html',
        privacy=viewo_legal.privacy(),
    )


@legal_.route('/download/<path:filename>')
def download_legal(filename):
    # TODO: SAFE JOIN REQUIRED?
    path = utilo.join(viewo_legal.ROOT, 'viewo_legal/text/')
    return flask.send_from_directory(
        path,
        filename,
        as_attachment=True,
    )
