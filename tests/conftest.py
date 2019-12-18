# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import exists
from os.path import join

from pytest import fixture

from viewo import create_application

pytest_plugins = 'pytester'  # pylint: disable=invalid-name


@fixture
def app(tmpdir):
    """Create and configure a new app instance for each test."""

    todo = join(tmpdir, 'todo')
    ready = join(tmpdir, 'ready')

    makedirs(todo)
    makedirs(ready)

    assert exists(todo), todo
    assert exists(ready), ready

    # create the app with common test config
    test_config = {
        'TESTING': True,
        'COMMON': tmpdir,
        'TODO': todo,
        'READY': ready,
    }
    application = create_application(config=test_config)

    yield application


@fixture
def client(app):  # pylint:disable=W0621
    """A test client for the app."""
    return app.test_client()


@fixture
def runner(app):  # pylint:disable=W0621
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
