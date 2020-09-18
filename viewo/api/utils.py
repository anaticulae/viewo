# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum


def simple_recursive(item):
    if isinstance(item, enum.Enum):
        return item.value
    if isinstance(item, list):
        return [simple_recursive(it) for it in item]
    try:
        item = vars(item)
    except TypeError:
        return item
    for key, value in item.items():
        item[key] = simple_recursive(value)
    return item
