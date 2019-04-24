# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from configo import share
from flask import Blueprint
from flask import render_template
from link import scan

documents = Blueprint('documents', __name__)


@documents.route('/documents', methods=['GET'])
def view_documents():
    todo, ready = scan(share())

    docs = todo + ready

    # sort by date
    docs = sorted(docs, key=lambda item: item.date, reverse=True)

    return render_template('documents/index.html', documents=docs)
