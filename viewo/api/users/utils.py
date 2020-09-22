# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import viewo.api.users.data
import viewo.config


def users():
    common_user = viewo.api.users.data.load_users(viewo.config.USERS)
    raw = [viewo.api.users.data.user_raw(item) for item in common_user]
    return raw
