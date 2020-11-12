# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests
import tests.api
import tests.waiting
import viewo.path
import viewo.waiting
import viewo.waiting.fastview


def test_waiting_fastview_status(valid, client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(viewo.path, 'todo', lambda: valid)
        result = tests.content(
            client,
            '/waiting/fastview/status/BAS45DFAC00JJ52K',
        )
    result = str(result)
    assert 'title' in result, str(result)
    assert 'pages' in result, str(result)
    assert 'content' in result, str(result)
    assert 'error' in result, str(result)
    assert 'good' in result, str(result)
    assert 'warning' in result, str(result)


def test_waiting_fastview_status_failure(valid, client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(viewo.path, 'todo', lambda: valid)
        result = tests.content(client, '/waiting/fastview/status/abcdc')
    assert result == {}, str(result)


def test_waiting_fastview(valid, test_client, monkeypatch):
    client = test_client
    tests.api.login(client)
    with monkeypatch.context() as context:
        context.setattr(viewo.path, 'todo', lambda: valid)
        result = tests.content(client, '/waiting/fastview/BAS45DFAC00JJ52K')

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


def test_waiting_load_groupstatus(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(viewo.path, 'todo', lambda: tests.EXAMPLE_TODO)
        loaded = viewo.waiting.fastview.load_fastview_result('BAS45DFAC00JJ52K')
    assert loaded
    assert len(loaded[0].error) == 1, str(loaded[0])
    assert loaded[1].error == [], str(loaded[1])
