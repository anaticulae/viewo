# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

from tests import EXAMPLE_READY
from tests import decode


def test_call_result(client):
    response = client.get('/result', follow_redirects=True)
    content = decode(response)
    assert content
    assert len(content) > 2000, content


def test_call_result_document_does_not_exist(client):
    response = client.get('/result/1020304050', follow_redirects=True)
    content = decode(response)
    assert content
    assert 'Fehler' in content


def test_call_result_document_and_imagedoes_not_exist(client):
    response = client.get('/result/1020304050/1.png', follow_redirects=True)
    content = decode(response)
    assert content
    assert 'Fehler' in content


def test_call_result_e508af0df454gi30(client, monkeypatch):

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {'SHARED_READY': EXAMPLE_READY})
        response = client.get('/result/E508AF0DF454GI30')
    content = decode(response)
    assert content


def test_call_result_e508af0df454gi30_image_access(client, monkeypatch):

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {'SHARED_READY': EXAMPLE_READY})
        response = client.get('/result/E508AF0DF454GI30/attention.png')
    assert response._status_code == 200, response  # pylint:disable=W0212
    # ensure that PNG is donwloaded
    assert b'PNG' in response.data, response
