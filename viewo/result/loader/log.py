# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import utila


def load_fromdocumentid(documentid: str) -> str:
    result = link.ready(documentid)
    if not utila.exists(result):
        return None
    if link.failed(documentid):
        path = utila.join(result, 'failed')
    else:
        path = utila.join(result, 'done')
    content = utila.file_read(path)
    return content
