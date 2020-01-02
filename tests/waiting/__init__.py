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

import tests
import viewo.waiting.data


def run_status(client, todo: str, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: todo)
        result = tests.content(client, '/waiting/status/12345678900')

    assert result, str(result)
    loaded = viewo.waiting.data.loads(result)
    return loaded


@pytest.fixture
def valid(testdir):
    root = str(testdir)
    assert os.path.exists(root), str(root)
    utila.copy_content(tests.EXAMPLE_TODO, root, recursive=True)
    return root


@pytest.fixture
def no_validation(valid):  # pylint:disable=W0621
    utila.file_remove(
        os.path.join(
            valid,
            '12345678900',
            viewo.waiting.VERIFY,
        ))
    return valid


@pytest.fixture
def invalid_validation(valid):  # pylint:disable=W0621
    utila.file_replace(
        os.path.join(
            valid,
            '12345678900',
            viewo.waiting.VERIFY,
        ),
        '{}',
    )
    return valid
