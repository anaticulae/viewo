# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

import tests
import viewo.path
import viewo.waiting.data


def run_status(client, todo: str, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(viewo.path, 'todo', lambda: todo)
        result = tests.content(client, '/waiting/status/BAS45DFAC00JJ52K')

    assert result, str(result)
    loaded = viewo.waiting.data.loads(result)
    return loaded
