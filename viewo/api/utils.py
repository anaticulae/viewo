# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum


def simple_recursive(item, not_none: bool = True, removes: set = None):
    if isinstance(item, enum.Enum):
        return item.value
    if isinstance(item, list):
        return [
            simple_recursive(it, not_none=not_none, removes=removes)
            for it in item
        ]
    if isinstance(item, tuple):
        return tuple([
            simple_recursive(it, not_none=not_none, removes=removes)
            for it in item
        ])
    try:
        item = vars(item)
    except TypeError:
        return item
    for key, value in item.items():
        item[key] = simple_recursive(value, not_none=not_none, removes=removes)
    if not_none:
        item = {key: value for key, value in item.items() if not value is None}
    if removes:
        item = {key: value for key, value in item.items() if key not in removes}
    return item
