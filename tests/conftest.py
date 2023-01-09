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
import power
import pytest
import utila
import utilatest
import viewo_api.user.create
# pylint:disable=W0611
from utilatest import mp
from utilatest import td

import tests
import viewo
import viewo.api.documents
import viewo.app
import viewo.config

pytest_plugins = ['pytester', 'xdist', 'localserver']  # pylint: disable=invalid-name

PACKAGE = viewo.PROCESS

RESOURCES_READY = [
    power.HOME018_PDF,
    power.HOME025_PDF,
    power.MASTER075_PDF,
]
RESOURCES_TODO = [
    power.DOCU007_PDF,
]

utilatest.setup(viewo.config.API_PREFIX)


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract_ready(files):
    readypath = power.generated(folder='ready')
    os.makedirs(readypath, exist_ok=True)
    with utila.GeorgFork() as fork:
        for path in files:
            fork.fork(
                method=run_queuemo,
                source=path,
                generated=readypath,
            )
    utila.directory_lock(readypath)


# TODO: REPLACE WITH VIEWO_API
PUBLIC = '00000000'


def extract_todo(files):
    todopath = power.generated(folder='todo')
    os.makedirs(todopath, exist_ok=True)
    with utila.GeorgFork() as fork:
        for path in files:
            fork.fork(
                method=run_queuemo,
                source=path,
                generated=todopath,
                owner=PUBLIC,
            )
    utila.directory_lock(todopath)


def run_queuemo(source, generated, owner=None):
    """Run queuemo to analyze document.

    Keep attentation to valid document/todo-name.
    """
    # 16 accepted document id length, disabled for testing
    todoname = utila.file_name(utila.path_parent(source))
    todoname += '_' + utila.file_name(source)
    workpath = os.path.join(generated, todoname)
    if os.path.exists(workpath):
        return
    utila.log(f'generate {workpath}')
    workspace = link.create_todo(
        source,
        todopath=generated,
        todoname=todoname,
        owner=owner,
    )
    # run single queuemo instance in workspace, write output to same workspace
    cmd = f'queuemo_single -i {workspace} -V'
    completed = utila.run(cmd)
    utila.debug(utila.format_completed(completed))


def zfill(text, width, char='0') -> str:
    fillme = max(width - len(text), 0)
    fillme = fillme * char
    return fillme + text


@pytest.fixture
def app(td):  # pylint:disable=W0621
    """Create and configure a new app instance for each test."""
    todo = td.tmpdir.join('todo')
    ready = td.tmpdir.join('ready')
    # create folder
    os.makedirs(todo)
    os.makedirs(ready)
    assert os.path.exists(todo), todo
    assert os.path.exists(ready), ready
    # create the app with common test config
    test_config = {
        'TESTING': True,
        'COMMON': td.tmpdir,
        'TODO': todo,
        'READY': ready,
    }
    # disable tracking in test run # TODO: MOVE TO CONFIG
    viewo.config.VISITORS_TRACKING = False
    application = viewo.app.create_app(config=test_config)
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
    viewo_api.user.create.create_user(
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
    result = utilatest.apiupload(client, '/documents', 'file', tests.MINIMAL)
    doc = result['document']
    return client, doc


@pytest.fixture
def findingclient(client):  # pylint:disable=W0621
    if not utila.exists(power.generated()):
        pytest.skip(reason='generate data')
    test_config = {
        'COMMON': power.generated(),
        'TODO': power.generated(folder='todo'),
        'READY': power.generated(folder='ready'),
    }
    client.application.config.update(test_config)
    return client


@pytest.fixture
def runner(app):  # pylint:disable=W0621
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
