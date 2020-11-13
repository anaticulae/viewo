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
    root = link.resultview(documentid, done=True)

    loaded = viewo.result.data.load_html(root)
    if pages is None:
        selected = loaded
    else:
        # ensure valid page numbers
        selected = [page for page in pages if 0 <= page < len(loaded)]
        selected = [loaded[page] for page in selected]
    # fix path to displayed images
    selected = [
        viewo.result.data.patch_images(content, documentid)
        for content in selected
    ]

    simple = viewo.api.utils.simple_recursive(selected)
    return simple


def pagecount(documentid: str) -> int:
    root = link.resultview(documentid, done=True)
    result = len(utila.file_list(root, include='html'))
    return result
