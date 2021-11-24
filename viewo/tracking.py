# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import queue
import threading

import flask
import utila

import viewo.api.visitors.data
import viewo.config


def before_each_request():
    if not viewo.config.VISITORS_TRACKING:
        # tracking is disabled
        return
    request = flask.request
    tracker().visit(request)


@utila.cacheme(maxsize=1)
def tracker():
    result = Tracker()
    result.start()
    return result


class Tracker:

    def __init__(self):
        self.store = queue.Queue()
        self.running = True

    def visit(self, request):
        env = vars(request)['environ']
        self.store.put(env)

    def consume(self):
        env = self.store.get()
        if not env:
            return
        agent = env.get('HTTP_USER_AGENT', 'NO_HTTP_USER_AGENT')
        ip = env.get('REMOTE_ADDR', 'NO_REMOTE_ADDR')
        method = env.get('REQUEST_METHOD', 'NO_USER_AGENT')
        path = env.get('PATH_INFO', 'NO_PATH_INFO')
        data = env.get('QUERY_STRING', 'NO_QUERY_STRING')
        # port = env['REMOTE_PORT']
        if not viewo.config.VISITORS_TRACKING_STATIC:
            if path.startswith('/static/'):
                return
        user = user_hash(ip, agent)
        date = utila.filetime()
        data = oneline(data)
        call = f'{method}:{path}?{data}' if data else f'{method}:{path}'
        # write to file system
        visitor = viewo.api.visitors.data.Visit(user, date, call)
        viewo.api.visitors.data.append(visitor)

    def run(self):
        while self.running:
            self.consume()

    def start(self):
        threading.Thread(target=self.run).start()

    def stop(self):
        self.running = False
        # ensure that waiting ends
        self.store.put(None)


def user_hash(ip, environment) -> int:
    return hash(f'{ip}:{environment}')


def oneline(data, limit: int = 256):
    r"""Remove newlines and shrink content to `limit` to avoid logging to
    mutch data.

    >>> oneline('first\nnewline')
    'first%NL%newline'
    """
    data = data.replace('\r\n', '%WNL%')
    data = data.replace('\n', '%NL%')
    data = data.replace(' ', '%WS%')
    data = data[0:limit]
    return data
