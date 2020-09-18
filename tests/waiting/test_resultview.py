# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

import viewo.result.data
import viewo.result.json
from tests import EXAMPLE_RESULT
from tests import content
from tests.waiting import valid  # pylint:disable=W0611


def validate_status(dumped: str):
    dumped = str(dumped)
    assert 'page' in dumped
    assert 'html' in dumped
    assert 'findings' in dumped
    assert 'title' in dumped
    assert 'location' in dumped


def test_waiting_resultview_load_resultview():
    loaded = viewo.result.data.load_resultview(
        EXAMPLE_RESULT,
        '1508790764',
    )
    assert loaded, str(loaded)
    pages = [item.page for item in loaded]
    # 3 html pages and one findings page
    assert pages == [0, 1, 2, 5]


def test_waiting_resultview_tojson():
    loaded = viewo.result.data.load_resultview(
        EXAMPLE_RESULT,
        '1508790764',
    )
    dumped = viewo.result.json.tojson(loaded)
    validate_status(dumped)
    assert len(dumped) > 450, str(dumped)


def test_waiting_resultview_status_failure(valid, client, monkeypatch):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = content(client, '/waiting/resultview/status/abcdc')
    assert not result


def test_waiting_resultview_status(valid, client, monkeypatch):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = content(client, '/waiting/resultview/status/12345678900')
    validate_status(result)


def test_waiting_resultview(valid, client, monkeypatch):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = content(client, '/waiting/resultview/12345678900')
    assert 'Gesamtdurchsicht' in result
    assert len(result) > 2000, str(result)
