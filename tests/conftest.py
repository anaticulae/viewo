# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
from os import makedirs
from os.path import exists
from os.path import join

import utila
from pytest import fixture

import tests
import viewo.app

pytest_plugins = 'pytester'  # pylint: disable=invalid-name


@fixture
def app(testdir):
    """Create and configure a new app instance for each test."""

    todo = join(testdir.tmpdir, 'todo')
    ready = join(testdir.tmpdir, 'ready')

    makedirs(todo)
    makedirs(ready)

    assert exists(todo), todo
    assert exists(ready), ready

    # create the app with common test config
    test_config = {
        'TESTING': True,
        'COMMON': testdir.tmpdir,
        'TODO': todo,
        'READY': ready,
    }
    application = viewo.app.create_application(config=test_config)

    yield application


@fixture
def client(app):  # pylint:disable=W0621
    """A test client for the app."""
    return app.test_client()


@fixture
def docclient(client):  # pylint:disable=W0621
    result = tests.apiupload(client, '/documents', 'file', tests.MINIMAL)
    doc = result['document']
    return client, doc


@fixture
def findingclient(client):  # pylint:disable=W0621
    utila.copy_content(
        tests.EXAMPLE_READY,
        os.path.join(os.getcwd(), 'ready'),
        recursive=True,
    )
    utila.copy_content(
        tests.EXAMPLE_TODO,
        os.path.join(os.getcwd(), 'todo'),
        recursive=True,
    )
    return client


@fixture
def runner(app):  # pylint:disable=W0621
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
