# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import power
import pytest
import utila
import utilatest

import tests
import viewo
import viewo.api.documents
import viewo.app
import viewo.config

pytest_plugins = ['pytester', 'xdist', 'localserver']  # pylint: disable=invalid-name

PACKAGE = viewo.PACKAGE

RESOURCES = [
    power.HOME018_PDF,
    power.HOME025_PDF,
    power.MASTER075_PDF,
]

utilatest.setup(viewo.config.API_PREFIX)


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(files):
    simplified = utilatest.simplify_testfile_names(files + [power.REPOSITORY])
    for source, dest in zip(files, simplified):
        run_queuemo(source, power.generated(), dest)
    assert os.path.exists(tests.EXAMPLE_READY), tests.EXAMPLE_READY
    assert os.path.exists(tests.EXAMPLE_RESULT), tests.EXAMPLE_RESULT


def run_queuemo(source, generated, dest):
    """Run queuemo to analyze document. Keep attentation to valid
    document/todo-name."""
    # 16 accepted document id length
    todoname = dest[-viewo.api.documents.DOCUMENTID_LENGTH:]
    # fill too short names
    todoname = zfill(todoname, viewo.api.documents.DOCUMENTID_LENGTH, char='_')
    workpath = os.path.join(generated, todoname)
    if os.path.exists(workpath):
        return
    utila.log(f'generate {workpath}')
    workspace = link.create_todo(source, todopath=generated, todoname=todoname)

    # run single queuemo instance in workspace, write output to same workspace
    cmd = f'queuemo_single -i {workspace} -V'
    completed = utila.run(cmd)
    utila.debug(utila.format_completed(completed))


def zfill(text, width, char='0') -> str:
    fillme = max(width - len(text), 0)
    fillme = fillme * char
    return fillme + text


@pytest.fixture
def app(testdir):
    """Create and configure a new app instance for each test."""

    todo = os.path.join(testdir.tmpdir, 'todo')
    ready = os.path.join(testdir.tmpdir, 'ready')

    os.makedirs(todo)
    os.makedirs(ready)

    assert os.path.exists(todo), todo
    assert os.path.exists(ready), ready

    # create the app with common test config
    test_config = {
        'TESTING': True,
        'COMMON': testdir.tmpdir,
        'TODO': todo,
        'READY': ready,
    }
    # disable tracking in test run # TODO: MOVE TO CONFIG
    viewo.config.VISITORS_TRACKING = False
    application = viewo.app.create_application(config=test_config)

    # ensure to create app context: TODO: THINK ABOUT IT
    with application.app_context():
        yield application


@pytest.fixture
def client(app):  # pylint:disable=W0621
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def test_client(client):  # pylint:disable=W0621
    """A test client for the app."""
    viewo.api.users.post.create_user(
        userid=tests.TEST_USER,
        password=tests.TEST_PASSWORD,
    )
    return client


@pytest.fixture
def user_client(test_client):  # pylint:disable=W0621
    result = tests.post(
        test_client,
        '/login',
        dict(user=tests.TEST_USER, password=tests.TEST_PASSWORD),
    )
    assert 'Login erfolgreich' in result, result
    # add users email
    tests.api.email_change(test_client)
    return test_client


@pytest.fixture
def payed_client(test_client):  # pylint:disable=W0621
    tests.post(test_client, '/payment', data=dict(choice=2))


@pytest.fixture
def docclient(client):  # pylint:disable=W0621
    result = tests.apiupload(client, '/documents', 'file', tests.MINIMAL)
    doc = result['document']
    return client, doc


@pytest.fixture
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


@pytest.fixture
def runner(app):  # pylint:disable=W0621
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
