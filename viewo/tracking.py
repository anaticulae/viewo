# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import utila

import viewo.api.visitors.data
import viewo.config


def before_each_request():
    if not viewo.config.VISITORS_TRACKING:
        # tracking is disabled
        return
    request = flask.request
    environment = vars(request)['environ']
    user_agent = environment['HTTP_USER_AGENT']
    ip = environment['REMOTE_ADDR']
    # port = environment['REMOTE_PORT']
    method, path = environment['REQUEST_METHOD'], environment['PATH_INFO']
    data = environment['QUERY_STRING']

    if not viewo.config.VISITORS_TRACK_STATIC_REQUESTS:
        if path.startswith('/static/'):
            return

    user = user_hash(ip, user_agent)
    date = utila.filetime()
    data = oneline(data)
    call = f'{method}:{path}?{data}' if data else f'{method}:{path}'

    visitor = viewo.api.visitors.data.Visit(user, date, call)
    viewo.api.visitors.data.append(visitor)


def user_hash(ip, environment) -> int:
    return hash(f'{ip}:{environment}')


def oneline(data, limit: int = 256):
    """Remove newlines and shrink content to `limit` to avoid logging to
    mutch data."""
    data = data.replace('\r\n', '%WNL%')
    data = data.replace('\n', '%NL%')
    data = data.replace(' ', '%WS%')
    data = data[0:limit]
    return data
