# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import link
import pytest
import utilo
import utilotest

import tests


@pytest.fixture
def valid(td):
    utilotest.fixture_requires(hoverpower.DOCU007_PDF, folder='todo')
    utilo.copy_content(
        tests.EXAMPLE_TODO,
        td.tmpdir,
        recursive=True,
        unlock=True,
    )
    return td.tmpdir


@pytest.fixture
def no_validation(valid):  # pylint:disable=W0621
    utilo.file_remove(
        os.path.join(
            valid,
            tests.TODO_DOCUMENT,
            link.PDFINFO_NAME,
        ))
    return valid


@pytest.fixture
def invalid_validation(valid):  # pylint:disable=W0621
    utilo.file_replace(
        os.path.join(
            valid,
            tests.TODO_DOCUMENT,
            link.PDFINFO_NAME,
        ),
        '{}',
    )
    return valid
