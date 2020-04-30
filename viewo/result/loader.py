# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os

import link
import serializeraw
import utila


def load_sentences(path: str) -> dict:
    # TODO: REFACTOR WITH FEEDBACK
    words = serializeraw.load_text(path)
    pagesentences = collections.defaultdict(list)
    for page, pagecontent in words:
        for _, sentences in pagecontent:
            for sentence in sentences:
                pagesentences[page].append(sentence)
    # enable KeyError
    pagesentences = dict(pagesentences)  # pylint:disable=R0204
    return pagesentences


def load_sentences_fromprocess(process: str) -> str:
    result = link.resultview(process)
    if not os.path.exists(result):
        return None
    path = os.path.join(result, 'words__word_result.yaml')
    if not os.path.exists(path):
        utila.error(f'could not load: {path}')
        return None
    return load_sentences(path)
