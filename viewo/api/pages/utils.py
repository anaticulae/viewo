# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utila

import viewo.api
import viewo.api.utils
import viewo.result.data


def load_html(documentid: str, pages: tuple = None) -> dict:
    root = link.resultview(documentid)  # pylint:disable=E1101

    loaded = viewo.result.data.load_html(root)
    selected = [loaded[page] for page in pages] if pages else loaded

    simple = viewo.api.utils.simple_recursive(selected)
    return simple


def pagecount(documentid: str) -> int:
    root = link.resultview(documentid)  # pylint:disable=E1101
    result = len(utila.file_list(root, include='html'))
    return result
