# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
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

import tests


@pytest.fixture
def valid(td):
    utilatest.fixture_requires(power.DOCU007_PDF, folder='todo')
    utila.copy_content(
        tests.EXAMPLE_TODO,
        td.tmpdir,
        recursive=True,
        unlock=True,
    )
    return td.tmpdir


@pytest.fixture
def no_validation(valid):  # pylint:disable=W0621
    utila.file_remove(
        os.path.join(
            valid,
            tests.TODO_DOCUMENT,
            link.PDFINFO_NAME,
        ))
    return valid


@pytest.fixture
def invalid_validation(valid):  # pylint:disable=W0621
    utila.file_replace(
        os.path.join(
            valid,
            tests.TODO_DOCUMENT,
            link.PDFINFO_NAME,
        ),
        '{}',
    )
    return valid
