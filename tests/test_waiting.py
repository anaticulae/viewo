# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import viewo.waiting


def test_waiting_status_jsonify():
    status = viewo.waiting.Status(
        status=viewo.waiting.State.running,
        state=[
            viewo.waiting.State.done,
            viewo.waiting.State.done,
            viewo.waiting.State.running,
            viewo.waiting.State.failed,
            viewo.waiting.State.waiting,
        ],
    )
    json = viewo.waiting.jsonify(status)
    assert 'states' in json
    assert 'status' in json
