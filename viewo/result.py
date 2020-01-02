# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import contextlib
from contextlib import suppress
from os import scandir
from os.path import exists
from os.path import join

from configo import ready
from flask import Blueprint
from flask import Markup
from flask import redirect
from flask import render_template
from flask import url_for
from utila import file_read
from utila import log

result_ = Blueprint('result', __name__)  # pylint:disable=C0103


@result_.route('/result')
@result_.route('/result/<int:document>')
@result_.route('/result/<int:document>/<string:action>')
@result_.route('/result/<int:document>/<string:action>/<int:major_id>')
@result_.route('/result/<int:document>/<string:action>/<int:major_id>/<int:minor_id>') # yapf:disable
@result_.route('/result/<int:document>/<string:action>/<int:major_id>/<int:minor_id>/<int:feature_id>') # yapf:disable
def view_result(
        document: int = None,
        action: str = None,  # pylint:disable=W0613
        major_id: int = None,
        minor_id: int = None,
        feature_id: int = None,
):
    if not document:
        return redirect(url_for('documents.view_documents'))

    result = load_result(document)
    if not result:
        return redirect(url_for('result.failure'))

    # prepare for javascript operation to open and close item's
    result, hidden = create_hidden_ref(result, major_id, minor_id, feature_id)

    return render_template(
        'result/index.html',
        docid=document,
        result=result,
        hidden=hidden,
    )


def create_hidden_ref(result, major_id, minor_id, feature_id):

    # TODO: Not very nice
    hidden = []
    for majorid, major in result:
        if not major['minor']:
            continue
        nbr = index(majorid)
        major['id'] = nbr
        hidden.append(nbr)
        for minorid, minor in major['minor']:
            nbr = index(majorid, minorid)
            minor['id'] = nbr
            hidden.insert(0, nbr)
            if not minor['feature']:
                continue
            for featureid, feature in minor['feature']:
                nbr = index(majorid, minorid, featureid)
                feature['id'] = nbr
                hidden.insert(0, nbr)

    not_hidden = []

    if major_id is not None:
        not_hidden.append(index(major_id))
    if major_id is not None and minor_id is not None:
        not_hidden.append(index(major_id, minor_id))
    if major_id is not None and minor_id is not None and feature_id is not None:
        not_hidden.append(index(major_id, minor_id, feature_id))

    # TODO: READ THE JINJA TO IMPROVE THIS
    for item in not_hidden:
        with suppress(ValueError):
            hidden.remove(item)
    return result, hidden


def index(major: int = None, minor: int = None, feature: int = None):
    if major is None:
        major = 0
        minor = -1
        feature = -1
    elif minor is None:
        minor = -1
        feature = -1
    elif feature is None:
        feature = -1

    return (major + 1) * 1000 + (minor + 1) * 100 + feature + 1


def load_result(documentid: int):
    ready_path = ready()
    assert exists(ready_path), ready_path

    document_path = join(ready_path, '%s' % documentid, 'result')
    if not exists(document_path):
        return None

    return structure(document_path)


def structure(path: str):

    def level_name(level):
        if level == 0:
            return 'minor'
        if level == 1:
            return 'feature'
        return 'to_deep'

    def go_deep(path, parent, level):
        with scandir(path) as files:
            for entry in files:
                if entry.is_file() or entry.name.startswith('.'):
                    continue
                children = []
                if not '_' in entry.name:
                    # result folder reuqires #NUMBER_#STRING
                    log('Skip non result folder %s' % entry.name)
                    continue
                index_, title = entry.name.split('_')

                content = load_content(join(path, entry.name))
                this = {
                    'title': title,
                }
                if content:
                    this['content'] = content

                with contextlib.suppress(ValueError):
                    # TODO: REMOVE LATER
                    parent.append((int(index_), this))

                go_deep(join(path, entry.name), children, level + 1)
                # if children:
                this[level_name(level)] = children

    result = []
    go_deep(path, result, 0)
    return result


def load_content(path: str) -> Markup:
    """Load index document out of feature path to render result

    Args:
        path(str): path to feature location where `index.html` is located
    Returns:
        loaded and not escaped html content, ready for jinja
        None if `index.html` not exists
    """
    html = join(path, 'index.html')
    if not exists(html):
        return None
    return Markup(file_read(html))


@result_.route('/result/failure')
def failure():
    return render_template('result/failure.html')
