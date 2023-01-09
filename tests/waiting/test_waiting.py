# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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


def test_waiting_status_running(no_validation, user_client, mp):
    loaded = tests.waiting.run_status(user_client, no_validation, mp)
    assert loaded.status == link.State.RUNNING
    assert loaded[0] == link.State.DONE
    assert loaded[1] == link.State.RUNNING


@tests.generated
def test_waiting_status_verified(user_client, td, mp):
    """Test a state where pdf is uploaded and validated.

    This requires the following resources:
        - pdf file with name process name in process folder like `docu_docu007`
        - pdfinfo.json with validation result of pdf file
    """
    todo = td.tmpdir.join(tests.TODO_DOCUMENT)
    os.makedirs(todo)
    utila.file_create(os.path.join(todo, tests.TODO_DOCUMENT))  # fake pdf file

    utila.file_copy(
        os.path.join(
            tests.EXAMPLE_TODO,
            tests.TODO_DOCUMENT,
            link.PDFINFO_NAME,
        ),
        os.path.join(todo, link.PDFINFO_NAME),
    )

    loaded = tests.waiting.run_status(user_client, td.tmpdir, mp)
    assert loaded.status == link.State.RUNNING
    assert loaded[0] == link.State.DONE
    assert loaded[1] == link.State.DONE
    assert loaded[2] == link.State.RUNNING


def test_waiting_status_verify_failed(
    invalid_validation,
    user_client,
    mp,
):
    loaded = tests.waiting.run_status(
        user_client,
        invalid_validation,
        mp,
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
    mp,
):
    with mp.context() as context:
        context.setattr(viewo.path, 'todo', lambda: invalid_validation)
        result = tests.content(
            user_client,
            f'/waiting/validation/{tests.TODO_DOCUMENT}',
        )
    assert ('Die hochgeladene Datei konnte <strong>'
            'nicht erfolgreich</strong>') in result, str(result)


def test_waiting_validation_result(valid, user_client, mp):
    with mp.context() as context:
        context.setattr(viewo.path, 'todo', lambda: valid)
        result = tests.content(
            user_client,
            f'/waiting/validation/{tests.TODO_DOCUMENT}',
        )

    assert ('Die PDF Datei konnte erfolgreich eingelesen'
            ' werden und wird nun analysiert.') in result, str(result)

    assert 'Pages' in result, str(result)
    assert 'Editor' in result, str(result)
