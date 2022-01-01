# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import threading
import time

import pytest
import utila
from viewvisitor.fixture import selenium_driver as driver  # pylint:disable=W0611


def viewo_start(port):
    cmd = f'viewo --host localhost --port {port}'
    completed = utila.run(cmd, expect=143)
    assert completed.returncode == 143


def viewo_shutdown():
    content = utila.run('ps -W').stdout
    for line in content.splitlines():
        if 'viewo' not in line:
            continue
        pid = line.split()[0]
        # TODO: WINDOWS
        utila.run(f'KILL -f {pid}')


LOCK = threading.Lock()
COUNTER = 4300


@contextlib.contextmanager
def newport():
    with LOCK:
        global COUNTER  # pylint:disable=global-statement
        COUNTER += 1
        yield COUNTER


@pytest.fixture(scope='session')
def webview():
    with newport() as port:
        runner = threading.Thread(target=viewo_start, args=(port,))
        runner.start()
    try:
        # wait for startup
        time.sleep(1)
        yield f'http://localhost:{port}/'
    except Exception as error:
        raise error from None


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    # remove old running instances
    viewo_shutdown()
