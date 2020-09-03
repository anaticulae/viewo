# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.caption


def pagecaptions_toraw(pagecaptions: iamraw.PageContentCaptions) -> list:
    result = []
    for item in pagecaptions:
        pagecontent = item.content
        if not pagecontent:
            continue
        collected = [caption_toraw(it) for it in pagecontent]
        result.append({
            'page': item.page,
            'captions': collected,
        })
    return result


def caption_toraw(caption: iamraw.Caption) -> dict:
    assert caption.line is not None
    result = {
        'line': caption.line,
        'raw': caption.raw,
    }
    if caption.lineend is not None:
        result['lineend'] = caption.lineend
    return result


assert not hasattr(iamraw.caption, 'pagecaptions_toraw'), 'TODO: remove patch'
iamraw.caption.pagecaptions_toraw = pagecaptions_toraw
assert hasattr(iamraw.caption, 'pagecaptions_toraw')
