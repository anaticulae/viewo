# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import legal

legal_ = flask.Blueprint('legal', __name__)  # pylint:disable=C0103


@legal_.route('/agb', methods=['GET'])
def agb():
    return flask.render_template('public/legal/agb.html', agb=legal.agb())


@legal_.route('/impressum', methods=['GET'])
def impressum():
    return flask.render_template(
        'public/legal/impressum.html',
        impressum=legal.impressum(),
    )


@legal_.route('/privacy', methods=['GET'])
def privacy():
    return flask.render_template(
        'public/legal/privacy.html',
        privacy=legal.privacy(),
    )


@legal_.route('/download/<path:filename>')
def download_legal(filename):
    return flask.send_from_directory(
        flask.safe_join(legal.ROOT, 'legal/text/'),
        filename,
        as_attachment=True,
    )
