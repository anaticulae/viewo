# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import link
import serializeraw
import utila


def load_fromdocumentid(documentid: str):
    result = link.resultview(documentid, done=True)
    if not utila.exists(result):
        return None
    path = iamraw.path.headerfooters(result)
    if not utila.exists(path):
        utila.error(f'could not load: {path}')
        return None
    return load_footenotes(path)


def load_footenotes(path: str):
    footerheaders = serializeraw.load_headerfooter(path)
    result = []
    for page in footerheaders:
        footer = page.footer
        if not footer:
            continue
        try:
            notes = footer.notes
        except AttributeError:
            continue
        result.append((page.page, notes))
    return result
