# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import exists
from os.path import join

import pytest

from viewo import create_application


@pytest.fixture
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


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
