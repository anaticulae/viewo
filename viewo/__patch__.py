# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def secure_hash(data: bytes, digits: int = 64, salt: str = None) -> str:  # pylint:disable=W0613
    # TODO: INTRODUCE SECURE ONE
    return utila.freehash(data, digits=digits)


utila.secure_hash = secure_hash
