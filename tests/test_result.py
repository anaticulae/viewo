# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import tests


def test_call_result(client):
    response = client.get('/view', follow_redirects=True)
    content = tests.decode(response)
    assert content
    assert len(content) > 2000, content


def test_call_result_document_does_not_exist(client):
    response = client.get('/view/1020304050', follow_redirects=True)
    content = tests.decode(response)
    assert content
    assert 'Fehler' in content


def test_call_result_document_and_imagedoes_not_exist(client):
    response = client.get('/view/1020304050/1.png', follow_redirects=True)
    content = tests.decode(response)
    assert content
    assert 'Fehler' in content


def test_call_result_e508af0df454gi30(client, monkeypatch):
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {'SHARED_READY': tests.EXAMPLE_READY})
        response = client.get(f'/view/{tests.TEST_DOCUMENT}')
    content = tests.decode(response)
    assert content


@tests.generated
def test_call_result_e508af0df454gi30_image_access(test_client):
    utila.copy_content(
        src=os.path.join(tests.EXAMPLE_ROOT, 'jobinfo.yaml'),
        dst=f'ready/{tests.TEST_DOCUMENT}',
    )
    utila.copy_content(
        src=tests.EXAMPLE_RESULT,
        dst=f'ready/{tests.TEST_DOCUMENT}/result',
        recursive=True,
    )
    response = test_client.get(
        f'/view/{tests.TEST_DOCUMENT}/7e98e4ad3dd91838.png',
        follow_redirects=True,
    )
    assert response.status_code == 200, response
    # ensure that PNG is donwloaded
    assert b'PNG' in response.data, response
