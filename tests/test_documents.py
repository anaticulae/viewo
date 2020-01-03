# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

import tests


def test_documents_view_no_documents(client):
    result = tests.content(client, '/documents')
    assert len(result) > 300, str(result)
    assert 'Keine Dokumente verfuegbar!' in result
    assert 'Fehler' not in result


def test_documents_view(client, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(configo, 'todo', lambda: tests.EXAMPLE_TODO)
        result = tests.content(client, '/documents')
    assert len(result) > 300, str(result)
    assert 'Keine Dokumente verfuegbar!' not in result, str(result)
    assert 'Fehler' not in result, str(result)
