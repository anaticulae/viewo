# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import configo

import tests
import viewo.waiting
import viewo.waiting.fastview
from tests.waiting import create_validation_result


def test_waiting_fastview_status(client, testdir, monkeypatch):
    root = str(testdir)
    create_validation_result(root)

    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: root)
        result = tests.content(client, '/waiting/fastview/status/12345678900')

    assert 'title' in result, str(result)
    assert 'pages' in result, str(result)
    assert 'content' in result, str(result)
    assert 'error' in result, str(result)
    assert 'good' in result, str(result)
    assert 'warning' in result, str(result)


def test_waiting_fastview_status_failure(client, testdir, monkeypatch):
    root = str(testdir)
    create_validation_result(root)

    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: root)
        result = tests.content(client, '/waiting/fastview/status/abcdc')

    assert '{}' in result, str(result)


def test_waiting_fastview(client, testdir, monkeypatch):
    root = str(testdir)
    create_validation_result(root)

    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: root)
        result = tests.content(client, '/waiting/fastview/12345678900')

    assert 'Schnelldurchsicht' in result, str(result)


def test_waiting_fastviewgroupstatus_jsonify():
    fastviewresult = viewo.waiting.FastViewStatus(
        content=[
            viewo.waiting.FastViewGroupStatus(
                title='Helmut in town',
                pages='1-5',
                error=['first', 'second', 'third'],
                good=['Mister good one.', 'good', 'better', 'best'],
                warning=[],
            )
        ],)
    json = viewo.waiting.fastview.fastviewstatus_tojson(fastviewresult)
    assert 'pages' in json
    assert 'title' in json
    assert '"Mister good one."' in json
