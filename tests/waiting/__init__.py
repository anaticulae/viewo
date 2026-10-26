# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos

import tests
import viewo.path
import viewo.waiting.data


def run_status(client, todo: str, mp):
    document = tests.TODO_DOCUMENT
    with mp.context() as context:
        context.setattr(viewo.path, 'todo', lambda: todo)
        result = tests.content(
            client,
            f'/waiting/status/{document}',
        )
    assert result, str(result)
    loaded = viewo.waiting.data.loads(result)
    return loaded
