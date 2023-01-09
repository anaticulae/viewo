# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila

import viewo.api
import viewo.api.utils
import viewo.config
import viewo.result.data


def load_html(documentid: str, pages: tuple = None, payed: bool = True) -> dict:
    root = link.resultview(documentid, done=True)

    loaded = viewo.result.data.load_html(root)
    if pages is None:
        selected = loaded
    else:
        # ensure valid page numbers
        selected = [page for page in pages if 0 <= page < len(loaded)]
        # select viewable pages
        selected = [loaded[page] for page in selected]
    # select viewable pages
    if not payed and not public(documentid):
        # TODO: THIS DOES NOT SUPPORT PARTIAL PAGES (0,1,2,5,6,8,10)
        start = 0 if pages is None else pages[0]
        selected = [
            item if free_view(
                page,
                payment=viewo.config.PAYMENT,
            ) else USER_PAY_REQUEST
            for page, item in enumerate(selected, start=start)
        ]
    # fix path to displayed images
    selected = [
        viewo.result.data.patch_images(content, documentid)
        for content in selected
    ]

    simple = utila.simplify(selected)
    return simple


USER_PAY_REQUEST = """\
<p class="center" style="padding-top:20%; font-size:24px;">Klicken Sie <a
href="/payment">hier um Vollzugriff</a> zu erhalten</p>
"""


def free_view(page: int, payment: bool = True) -> bool:
    """Every third page is free and viewable without paying.

    >>> free_view(0)
    True
    >>> free_view(1)
    False
    >>> free_view(2)
    False
    >>> free_view(2, payment=False)
    True
    """
    if not payment:
        # all pages are free for all
        return True
    if page % 3 == 0:  # pylint:disable=C2001
        return True
    return False


def pagecount(documentid: str) -> int:
    root = link.resultview(documentid, done=True)
    result = len(utila.file_list(os.path.join(root, 'view'), include='html'))
    return result


def public(documentid: str) -> bool:
    """Check if document is not bound to user account and login is not
    required."""
    # TODO: MOVE TO LINK
    # TODO: VERIFY WITH UNIT TEST: After logging in, public documents
    # where not visbile anymore, purchase was required
    owner = link.owner(documentid)
    if owner == link.PUBLIC_OWNER:
        return True
    return False
