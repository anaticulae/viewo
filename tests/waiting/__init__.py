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
import viewo.waiting.data


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
