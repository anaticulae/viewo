# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila

import tests
import tests.api
import tests.waiting
import viewo.path
import viewo.waiting
import viewo.waiting.data
import viewo.waiting.fastview


def test_waiting_status_jsonify():
    status = viewo.waiting.Status(
        status=link.State.RUNNING,
        state=[
            link.State.DONE,
            link.State.DONE,
            link.State.RUNNING,
            link.State.FAILED,
            link.State.WAITING,
        ],
    )
    json = viewo.waiting.data.jsonify(status)
    assert 'states' in json
    assert 'status' in json


def test_waiting_status_invalid(client):
    result = tests.content(client, '/waiting')
    assert 'Fehler' in result


def test_waiting_status_invalid_resource(user_client):
    result = tests.content(user_client, '/waiting/status/1337')
    assert not result


def test_waiting_status(no_validation, user_client, monkeypatch):
    loaded = tests.waiting.run_status(user_client, no_validation, monkeypatch)
    assert loaded.status == link.State.RUNNING
    assert loaded[0] == link.State.DONE
    assert loaded[1] == link.State.RUNNING


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
            link.PDFINFO_NAME,
        ),
        os.path.join(todo, link.PDFINFO_NAME),
    )

    loaded = tests.waiting.run_status(user_client, root, monkeypatch)
    assert loaded.status == link.State.RUNNING
    assert loaded[0] == link.State.DONE
    assert loaded[1] == link.State.DONE
    assert loaded[2] == link.State.RUNNING


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
    assert loaded.status == link.State.FAILED
    assert loaded[0] == link.State.DONE
    assert loaded[1] == link.State.FAILED
    assert loaded[2] == link.State.FAILED
    assert loaded[3] == link.State.FAILED
    assert loaded[4] == link.State.FAILED
    assert loaded[5] == link.State.FAILED


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
