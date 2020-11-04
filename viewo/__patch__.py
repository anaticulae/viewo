# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def simplify_pages(numbers: tuple) -> str:
    """\
    >>> simplify_pages(10)
    '10'
    >>> simplify_pages((1, 2, 3, 4, 5))
    '1:6'
    >>> simplify_pages([1, 3, 5, 6, 7])
    '1,3,5:8'
    >>> simplify_pages(None)
    ':'
    """
    if isinstance(numbers, int):
        numbers = [numbers]
    if not numbers:
        return ':'
    diffed = utila.groupby_diff(numbers, diff=1)
    result = []
    for item in diffed:
        if len(item) == 1:
            result.append(str(item[0]))
        else:
            result.append(f'{item[0]}:{item[-1]+1}')
    return ','.join(result)


utila.simplify_pages = simplify_pages
