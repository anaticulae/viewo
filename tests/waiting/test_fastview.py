# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import configo

import viewo.waiting
import viewo.waiting.fastview
from tests import EXAMPLE_TODO
from tests import content
from tests.waiting import valid  # pylint:disable=W0611


def test_waiting_fastview_status(valid, client, monkeypatch):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = content(client, '/waiting/fastview/status/12345678900')

    assert 'title' in result, str(result)
    assert 'pages' in result, str(result)
    assert 'content' in result, str(result)
    assert 'error' in result, str(result)
    assert 'good' in result, str(result)
    assert 'warning' in result, str(result)


def test_waiting_fastview_status_failure(valid, client, monkeypatch):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = content(client, '/waiting/fastview/status/abcdc')

    assert '{}' in result, str(result)


def test_waiting_fastview(valid, client, monkeypatch):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = content(client, '/waiting/fastview/12345678900')

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
        context.setattr(configo, 'todo', lambda: EXAMPLE_TODO)
        loaded = viewo.waiting.fastview.load_fastview_result('12345678900')
    assert loaded
    assert len(loaded[0].error) == 1, str(loaded[0])
    assert loaded[1].error == [], str(loaded[1])
