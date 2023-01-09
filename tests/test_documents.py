# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests


def test_documents_view_no_documents(client):
    result = tests.content(client, '/documents')
    assert len(result) > 300, str(result)
    assert 'Keine Dokumente verfügbar!' in result
    assert 'Fehler' not in result


def test_documents_view_with_documents(findingclient, td):  # pylint:disable=W0613
    result = tests.content(findingclient, '/documents')
    assert len(result) > 300, str(result)
    assert 'Keine Dokumente verfügbar!' not in result, str(result)
    assert 'Fehler' not in result, str(result)


def test_documents_compare(client):
    result = tests.content(client, '/document_compare')
    assert len(result) > 300, str(result)
    assert 'Dokument Vergleich' in result
