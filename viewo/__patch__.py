# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import link
import utila


def delete(document: str) -> bool:  # pylint:disable=W0621
    """Set deleting flag to mark fastview and resultview as deleted.

    This function works asynchronous. The content is removed later by
    `ResourceSyncScheduler`.

    Args:
        document(str): document id to identify document.
    Returns:
        True if deleting mark is successfully created.
        False if `document` is already marked as deleted.
    """
    if link.current(document) == link.ProcessState.DELETED:
        return False

    todo_path = link.todo(document)
    ready_path = link.ready(document)

    if not (os.path.exists(todo_path) or os.path.exists(ready_path)):
        return False

    if os.path.exists(todo_path):
        utila.file_create(link.todo_deleted(document))

    if os.path.exists(ready_path):
        # processing is not completed(error or cancelled)
        utila.file_create(link.ready_deleted(document))

    return True


link.delete = delete


def document(document: str) -> str:  # pylint:disable=W0621
    for method in [link.ready, link.todo]:
        if os.path.exists(method(document)):
            return method(document)
    return None


link.document = document


def resultview(document: str) -> str:  # pylint:disable=W0621
    source = link.todo(document)
    if os.path.exists(link.ready(document)):
        source = link.ready(document)
    return os.path.join(source, 'result')


link.resultview = resultview
