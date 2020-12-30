# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import tests
import tests.api
import tests.waiting
import viewo.path
import viewo.waiting
import viewo.waiting.fastview


def test_waiting_status_jsonify():
    status = viewo.waiting.Status(
        status=viewo.waiting.State.RUNNING,
        state=[
            viewo.waiting.State.DONE,
            viewo.waiting.State.DONE,
            viewo.waiting.State.RUNNING,
            viewo.waiting.State.FAILED,
            viewo.waiting.State.WAITING,
        ],
    )
    json = viewo.waiting.data.jsonify(status)
    assert 'states' in json
    assert 'status' in json


def test_waiting_status_fromstr():
    with pytest.raises(ValueError):
        viewo.waiting.State.fromstr('')


def test_waiting_status_invalid(client):
    result = tests.content(client, '/waiting')
    assert 'Fehler' in result


def test_waiting_status_invalid_resource(user_client):
    result = tests.content(user_client, '/waiting/status/1337')
    assert not result


def test_waiting_status(no_validation, user_client, monkeypatch):
    loaded = tests.waiting.run_status(user_client, no_validation, monkeypatch)
    assert loaded.status == viewo.waiting.State.RUNNING
    assert loaded[0] == viewo.waiting.State.DONE
    assert loaded[1] == viewo.waiting.State.RUNNING


def test_waiting_status_verified(user_client, testdir, monkeypatch):
    """Test a state where pdf is uploaded and validated.

    This requires the following resources:
        - pdf file with name process name in process folder like `BAS45DFAC00JJ52K`
        - pdfinfo.json with validation result of pdf file
    """
    root = str(testdir)
    todo = os.path.join(root, 'BAS45DFAC00JJ52K')
    os.makedirs(todo)
    utila.file_create(os.path.join(todo, 'BAS45DFAC00JJ52K'))  # fake pdf file

    utila.file_copy(
        os.path.join(
            tests.EXAMPLE_TODO,
            'BAS45DFAC00JJ52K',
            viewo.waiting.VERIFY,
        ),
        os.path.join(todo, viewo.waiting.VERIFY),
    )

    loaded = tests.waiting.run_status(user_client, root, monkeypatch)
    assert loaded.status == viewo.waiting.State.RUNNING
    assert loaded[0] == viewo.waiting.State.DONE
    assert loaded[1] == viewo.waiting.State.DONE
    assert loaded[2] == viewo.waiting.State.RUNNING


def test_waiting_status_verify_failed(
        invalid_validation,
        user_client,
        monkeypatch,
):
    loaded = tests.waiting.run_status(
        user_client,
        invalid_validation,
        monkeypatch,
    )
    assert loaded.status == viewo.waiting.State.FAILED
    assert loaded[0] == viewo.waiting.State.DONE
    assert loaded[1] == viewo.waiting.State.FAILED
    assert loaded[2] == viewo.waiting.State.FAILED
    assert loaded[3] == viewo.waiting.State.FAILED
    assert loaded[4] == viewo.waiting.State.FAILED
    assert loaded[5] == viewo.waiting.State.FAILED


def test_waiting_validation_invalid_result(
        invalid_validation,
        user_client,
        monkeypatch,
):
    with monkeypatch.context() as context:
        context.setattr(viewo.path, 'todo', lambda: invalid_validation)
        result = tests.content(
            user_client,
            '/waiting/validation/BAS45DFAC00JJ52K',
        )
    assert ('Die hochgeladene Datei konnte <strong>'
            'nicht erfolgreich</strong>') in result, str(result)


def test_waiting_validation_result(valid, user_client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(viewo.path, 'todo', lambda: valid)
        result = tests.content(
            user_client,
            '/waiting/validation/BAS45DFAC00JJ52K',
        )

    assert ('Die PDF Datei konnte erfolgreich eingelesen'
            ' werden und wird nun analysiert.') in result, str(result)

    assert 'Pages' in result, str(result)
    assert 'Editor' in result, str(result)
