# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

from pytest import raises

from viewo.config import environment


def test_without_folder_configuration(monkeypatch):
    """The communication folder for the view and pdf-mining is defined by
    shared folder `SHARED_TODO` and `SHARED_READY`"""

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {})

        with raises(SystemExit):
            environment()


def test_with_wrong_folder_configuration(monkeypatch):
    """The communication folder for the view and pdf-mining is defined by
    shared folder `SHARED_TODO` and `SHARED_READY`"""

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {
            'SHARED_TODO': 'NO_PATH',
            'SHARED_READY': 'WRONG_PATH',
        })

        with raises(SystemExit):
            environment()
