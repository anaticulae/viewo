# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import threading

import pytest
import utila
from viewvisitor.fixture import selenium_driver as driver  # pylint:disable=W0611


def viewo_start(port):
    cmd = f'viewo --host localhost --port {port}'
    print(cmd)
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

COUNTER = 6000


@contextlib.contextmanager
def newport():
    with LOCK:
        global COUNTER
        COUNTER += 1
        yield COUNTER


@pytest.fixture()
def webview(client):
    with newport() as port:
        viewo_shutdown()
        runner = threading.Thread(target=viewo_start, args=(port,))
        runner.start()
        try:
            yield f'http://localhost:{port}'
            viewo_shutdown()
        except Exception as error:
            viewo_shutdown()
            raise error from None
