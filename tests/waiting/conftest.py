# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import tests
import viewo.waiting


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
            'BAS45DFAC00JJ52K',
            viewo.waiting.VERIFY,
        ))
    return valid


@pytest.fixture
def invalid_validation(valid):  # pylint:disable=W0621
    utila.file_replace(
        os.path.join(
            valid,
            'BAS45DFAC00JJ52K',
            viewo.waiting.VERIFY,
        ),
        '{}',
    )
    return valid
