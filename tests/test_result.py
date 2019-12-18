# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

from pytest import fixture

from tests import EXAMPLE_READY
from tests import EXAMPLE_RESULT
from tests import decode
from viewo.result import create_hidden_ref
from viewo.result import index
from viewo.result import structure


def test_index():
    assert index(None, None, None) == 1000
    assert index(0, None, None) == 1000
    assert index(0, 0, None) == 1100
    assert index(0, 0, 0) == 1101
    assert index(0, 0, 1) == 1102
    assert index(1, 0, None) == 2100
    assert index(1, 1, None) == 2200
    assert index(1, 0, 0) == 2101
    assert index(1, 1, 0) == 2201


@fixture
def example():
    result = [
        (0, {
            'title':
            'Layout',
            'right':
            120,
            'wrong':
            30,
            'question':
            7,
            'minor': [
                (0, {
                    'title':
                    'Bordercheck',
                    'right':
                    120,
                    'wrong':
                    30,
                    'question':
                    7,
                    'feature': [
                        (0, {
                            'title': 'No overwriting',
                            'right': [],
                            'wrong': [],
                            'question': [],
                        }),
                        (1, {
                            'title': 'Good footer',
                            'right': [],
                            'wrong': [],
                            'question': [],
                        }),
                    ],
                }),
                (1, {
                    'title':
                    'Verzeichnisse',
                    'right':
                    5,
                    'wrong':
                    2,
                    'question':
                    7,
                    'feature': [
                        (0, {
                            'title': 'Inhaltsverzeichnis',
                            'right': [],
                            'wrong': [],
                            'question': [],
                        }),
                        (1, {
                            'title': 'Abbildungsverzeichnis',
                            'right': [],
                            'wrong': [],
                            'question': [],
                        }),
                    ],
                }),
            ],
        }),
        (1, {
            'title':
            'Writing',
            'right':
            30,
            'wrong':
            10,
            'question':
            3,
            'minor': [
                (0, {
                    'title': 'Words',
                    'right': 120,
                    'wrong': 30,
                    'question': 7,
                    'feature': [],
                }),
            ],
        }),
        (2, {
            'title': 'Statistica',
            'right': 2222,
            'wrong': 2,
            'question': 0,
            'minor': [],
        }),
    ]
    return result


def test_hidden_ref_no_selection(example):  # pylint:disable=W0621
    _, hidden = create_hidden_ref(example, None, None, None)

    # All children are hidden
    assert len(hidden) == 9


def test_hidden_ref_with_selection(example):  # pylint:disable=W0621
    _, hidden = create_hidden_ref(example, 0, 0, 0)
    assert len(hidden) == 6


def test_call_result(client):
    response = client.get('/result')
    content = decode(response)
    assert content
    # assert len(content) > len(BASE_TEMPLATE), content


def test_call_result_document_does_not_exist(client):
    response = client.get('/result/1020304050', follow_redirects=True)
    content = decode(response)
    assert content
    assert 'Fehler' in content


def test_structure():
    result = structure(EXAMPLE_RESULT)
    assert len(result) == 3  # 02_layout, 04_writing, 06_statistica
    assert result[0][0] == 2, result  # 02_layout
    assert 'minor' in result[0][1], result  # 02_layout
    assert 'title' in result[0][1], result  # 02_layout
    assert 'minor' in result[2][1]  # 06_statistica
    assert result[2][0] == 6  # 06_statistica


def test_call_result_1508790764(client, monkeypatch):

    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(os, 'environ', {
            'SHARED_READY': EXAMPLE_READY,
        })
        response = client.get('/result/1508790764')
    content = decode(response)
    assert content
