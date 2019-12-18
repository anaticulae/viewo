# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila

import tests
import viewo.waiting


def create_validation_result(path: str):
    assert os.path.exists(path), str(path)
    utila.copy_content(tests.EXAMPLE_TODO, path, recursive=True)


def create_no_validation_result(path: str):
    assert os.path.exists(path), str(path)
    utila.copy_content(tests.EXAMPLE_TODO, path, recursive=True)
    utila.file_remove(os.path.join(
        path,
        '12345678900',
        viewo.waiting.VERIFY,
    ))


def create_invalid_validation_result(path: str):
    assert os.path.exists(path), str(path)
    utila.copy_content(tests.EXAMPLE_TODO, path, recursive=True)
    utila.file_replace(
        os.path.join(
            path,
            '12345678900',
            viewo.waiting.VERIFY,
        ),
        '{}',
    )


def run_status(client, todo: str, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: todo)
        result = tests.content(client, '/waiting/status/12345678900')

    assert result, str(result)
    loaded = viewo.waiting.data.loads(result)
    return loaded


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


def test_waiting_status_invalid(client):
    result = tests.content(client, '/waiting')
    assert 'Fehler' in result


def test_waiting_status_invalid_ressource(client):
    result = tests.content(client, '/waiting/status/1337')
    assert result == '{}'


def test_waiting_status(testdir, client, monkeypatch):
    root = str(testdir)
    create_no_validation_result(root)

    loaded = run_status(client, root, monkeypatch)

    assert loaded.status == viewo.waiting.State.running
    assert loaded[0] == viewo.waiting.State.done
    assert loaded[1] == viewo.waiting.State.running


def test_waiting_status_verified(client, testdir, monkeypatch):
    loaded = run_status(client, tests.EXAMPLE_TODO, monkeypatch)

    assert loaded.status == viewo.waiting.State.running
    assert loaded[0] == viewo.waiting.State.done
    assert loaded[1] == viewo.waiting.State.done
    assert loaded[2] == viewo.waiting.State.running


def test_waiting_status_verify_failed(client, testdir, monkeypatch):
    root = str(testdir)
    create_invalid_validation_result(root)

    loaded = run_status(client, root, monkeypatch)

    assert loaded.status == viewo.waiting.State.failed
    assert loaded[0] == viewo.waiting.State.done
    assert loaded[1] == viewo.waiting.State.failed
    assert loaded[2] == viewo.waiting.State.failed
    assert loaded[3] == viewo.waiting.State.failed
    assert loaded[4] == viewo.waiting.State.failed
    assert loaded[5] == viewo.waiting.State.failed


def test_waiting_validation_invalid_result(client, testdir, monkeypatch):
    root = str(testdir)
    create_invalid_validation_result(root)

    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: root)
        result = tests.content(client, '/waiting/validation/12345678900')

    assert ('Die hochgeladene Datei konnte nicht erfolgreich als PDF Datei'
           ) in result, str(result)


def test_waiting_validation_result(client, testdir, monkeypatch):
    root = str(testdir)
    create_validation_result(root)

    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: root)
        result = tests.content(client, '/waiting/validation/12345678900')

    assert ('Die PDF Datei konnte erfolgreich eingelesen'
            ' werden und wird nun analysiert.') in result, str(result)

    assert 'Pages' in result, str(result)
    assert 'Editor' in result, str(result)
