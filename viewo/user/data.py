# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import flask_login

import viewo.api.users.data


@dataclasses.dataclass
class FlaskUser(flask_login.UserMixin):
    identifier: str = None

    def get_id(self):
        return self.identifier

    @property
    def payed(self):
        user = viewo.api.users.data.user_fromid(self.identifier)
        if not user:
            return 0
        return user.payed

    @property
    def is_admin(self):
        return False
