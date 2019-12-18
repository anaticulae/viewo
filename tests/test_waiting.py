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

VERIFIED_12345678900 = """\
{"pages": "7", "generator": "latex", "version": {"major": 1, "minor": 5}}
"""


def test_waiting_status_jsonify():
    status = viewo.waiting.Status(
        status=viewo.waiting.State.running,
        state=[
            viewo.waiting.State.done,
            viewo.waiting.State.done,
            viewo.waiting.State.running,
            viewo.waiting.State.failed,
            viewo.waiting.State.waiting,
        ],
    )
    json = viewo.waiting.jsonify(status)
    assert 'states' in json
    assert 'status' in json


def test_waiting_status_invalid(client):
    result = tests.content(client, '/waiting')
    assert 'Fehler' in result


def test_waiting_status_invalid_ressource(client):
    result = tests.content(client, '/waiting/status/1337')
    assert result == '{}'


def test_waiting_status(client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: tests.EXAMPLE_TODO)
        result = tests.content(client, '/waiting/status/12345678900')
    assert result, str(result)
    loaded = viewo.waiting.loads(result)
    assert loaded.status == viewo.waiting.State.running

    assert loaded[0] == viewo.waiting.State.done
    assert loaded[1] == viewo.waiting.State.running
