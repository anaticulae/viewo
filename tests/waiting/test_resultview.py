# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila

import tests
import tests.api
import viewo.result.data
import viewo.result.json


def validate_status(dumped: str):
    dumped = str(dumped)
    assert 'page' in dumped
    assert 'html' in dumped
    assert 'findings' in dumped
    assert 'title' in dumped
    assert 'location' in dumped


def test_waiting_resultview_load_resultview():
    loaded = viewo.result.data.load_resultview(
        tests.EXAMPLE_RESULT,
        tests.TEST_DOCUMENT,
    )
    assert loaded, str(loaded)
    pages = [item.page for item in loaded]
    # 25 html pages and x findings page
    # TODO: REPLACE WITH UTILA CODE
    assert pages == list(utila.ranged_tuple(0, 25))


def test_waiting_resultview_tojson():
    loaded = viewo.result.data.load_resultview(
        tests.EXAMPLE_RESULT,
        tests.TEST_DOCUMENT,
    )
    dumped = viewo.result.json.tojson(loaded)
    validate_status(dumped)
    assert len(dumped) > 450, str(dumped)


def test_waiting_resultview_status_failure(valid, user_client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = tests.content(
            user_client,
            '/waiting/resultview/status/abcdc',
        )
    assert not result


def test_waiting_resultview_status(valid, user_client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = tests.content(
            user_client,
            '/waiting/resultview/status/BAS45DFAC00JJ52K',
        )
    validate_status(result)


def test_waiting_resultview(valid, user_client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = tests.content(
            user_client,
            '/waiting/resultview/BAS45DFAC00JJ52K',
        )
    assert 'Gesamtdurchsicht' in result
    assert len(result) > 2000, str(result)
