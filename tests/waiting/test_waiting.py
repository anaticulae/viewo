# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import pytest
import utila

import viewo.waiting
import viewo.waiting.fastview
from tests import EXAMPLE_TODO
from tests import content
# pylint:disable=W0611
from tests.waiting import invalid_validation
from tests.waiting import no_validation
from tests.waiting import run_status
from tests.waiting import valid


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
    json = viewo.waiting.data.jsonify(status)
    assert 'states' in json
    assert 'status' in json


def test_waiting_status_fromstr():
    with pytest.raises(ValueError):
        viewo.waiting.State.fromstr('')


def test_waiting_status_invalid(client):
    result = content(client, '/waiting')
    assert 'Fehler' in result


def test_waiting_status_invalid_resource(client):
    result = content(client, '/waiting/status/1337')
    assert result == '{}'


def test_waiting_status(no_validation, client, monkeypatch):  # pylint:disable=W0621
    loaded = run_status(client, no_validation, monkeypatch)

    assert loaded.status == viewo.waiting.State.running
    assert loaded[0] == viewo.waiting.State.done
    assert loaded[1] == viewo.waiting.State.running


def test_waiting_status_verified(client, testdir, monkeypatch):
    """Test a state where pdf is uploaded and validated.

    This requires the following resources:
        - pdf file with name process name in process folder like `12345678900`
        - pdfinfo.json with validation result of pdf file
    """
    root = str(testdir)
    todo = os.path.join(root, '12345678900')
    os.makedirs(todo)
    utila.file_create(os.path.join(todo, '12345678900'))  # fake pdf file

    utila.file_copy(
        os.path.join(EXAMPLE_TODO, '12345678900', viewo.waiting.VERIFY),
        os.path.join(todo, viewo.waiting.VERIFY),
    )
    loaded = run_status(client, root, monkeypatch)
    assert loaded.status == viewo.waiting.State.running
    assert loaded[0] == viewo.waiting.State.done
    assert loaded[1] == viewo.waiting.State.done
    assert loaded[2] == viewo.waiting.State.running


def test_waiting_status_verify_failed(invalid_validation, client, monkeypatch):  # pylint:disable=W0621
    loaded = run_status(client, invalid_validation, monkeypatch)

    assert loaded.status == viewo.waiting.State.failed
    assert loaded[0] == viewo.waiting.State.done
    assert loaded[1] == viewo.waiting.State.failed
    assert loaded[2] == viewo.waiting.State.failed
    assert loaded[3] == viewo.waiting.State.failed
    assert loaded[4] == viewo.waiting.State.failed
    assert loaded[5] == viewo.waiting.State.failed


def test_waiting_validation_invalid_result(
        invalid_validation,
        client,
        monkeypatch,
):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: invalid_validation)
        result = content(client, '/waiting/validation/12345678900')
    assert ('Die hochgeladene Datei konnte <strong>'
            'nicht erfolgreich</strong>') in result, str(result)


def test_waiting_validation_result(valid, client, monkeypatch):  # pylint:disable=W0621
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: valid)
        result = content(client, '/waiting/validation/12345678900')

    assert ('Die PDF Datei konnte erfolgreich eingelesen'
            ' werden und wird nun analysiert.') in result, str(result)

    assert 'Pages' in result, str(result)
    assert 'Editor' in result, str(result)
