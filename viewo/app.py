# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import flask
import flask_bootstrap
import flask_moment
import utilo

try:
    import viewo_waiter
    import viewo_waiter.api.document.post
except ImportError:
    utilo.error('could not import viewo_waiter')

try:
    import admin_helpdesk
    import admin_helpdesk.api
    from admin_helpdesk.api import *  # pylint:disable=wildcard-import,W0614,C0412
except ImportError:
    utilo.error('could not import admin_helpdesk')

import viewo
import viewo.__patch__
import viewo.api_.findings.data
import viewo.cache
import viewo.config
import viewo.path
import viewo.tracking
import viewo.user.loginmanager
from viewo.api.documents import *  # pylint:disable=wildcard-import,W0614
from viewo.api.findings import *  # pylint:disable=wildcard-import
from viewo.api.pageviews import *  # pylint:disable=wildcard-import
from viewo.api.result import result_
from viewo.api.users import *  # pylint:disable=wildcard-import
from viewo.api.visitors import *  # pylint:disable=wildcard-import
from viewo.api.waiting import waiting_
from viewo.api.writing import writing_
from viewo.user import *  # pylint:disable=wildcard-import
from viewo.view.contact import contact_
from viewo.view.documents import documents_
from viewo.view.legal import legal_
from viewo.view.payment import payment
from viewo.view.welcome import welcome


class Application(flask.Flask):

    def __init__(self):
        super().__init__(__name__)
        self.secret_key = viewo.config.SECRET_KEY
        self.config.setdefault('MAX_CONTENT_LENGTH', viewo.config.FILE_SIZE_MAX)
        self.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)
        # configure extensions
        flask_bootstrap.Bootstrap(app=self)
        flask_moment.Moment(app=self)
        if viewo.config.OPTIMIZE_DATA:
            # optimize transfer
            self.after_request(viewo.optimize.optimize)
        self.create_template_test()

    def create_template_test(self):
        self.add_template_test(Application.ready_exists, name='ready_exists')
        self.context_processor(Application.context_data)
        self.add_template_global(Application.pagenumber, name='pagenumber')

    @staticmethod
    def ready_exists(path) -> bool:
        result = os.path.join(configos.ready(), path)
        return os.path.exists(result)

    @staticmethod
    def context_data() -> dict:
        result = dict(
            payment_active=viewo.config.PAYMENT,
            talker_active=viewo.config.TALKER,
        )
        return result

    @staticmethod
    def pagenumber(pdfpage, documentid) -> str:
        import viewo.result.loader.pagenumbers  # pylint:disable=W0621
        result = viewo.result.loader.pagenumbers.userpage(
            pdfpage=pdfpage,
            documentid=documentid,
        )
        return result


def create_app(config=None) -> flask.Flask:
    """Setup flask application

    1. Set template and static folder
    2. Configure application
    3. Setup global env
    4. Register blueprint for routing the user requests
    """
    viewo.config.config_show()
    # Flask determines template- and static-folder automatically.
    appi = Application()
    # configure app instance
    configure(appi, config)
    # setup error handler
    init_error_handler(appi)
    # view
    appi.register_blueprint(viewo_user)
    appi.register_blueprint(documents_)
    appi.register_blueprint(legal_)
    appi.register_blueprint(contact_)
    appi.register_blueprint(result_)
    appi.register_blueprint(waiting_)
    appi.register_blueprint(welcome)
    appi.register_blueprint(writing_)
    appi.register_blueprint(payment)
    # extenral
    # Add external route with the same name to internal route
    # TODO: RENAME LATER, DON'T KNOW TO RESOLVE THIS, YET
    try:
        api_documents.deferred_functions.extend(viewo_waiter.api_documents.deferred_functions)  # yapf:disable
    except NameError:
        utilo.error('could not register viewo_waiter')
    # data API
    # internal
    appi.register_blueprint(api_documents, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_findings, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_pageviews, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_users, url_prefix=viewo.config.API_PREFIX)
    appi.register_blueprint(api_visitors, url_prefix=viewo.config.API_PREFIX)
    # messages
    try:
        appi.register_blueprint(
            admin_helpdesk.api.api_message,
            url_prefix=viewo.config.API_PREFIX,
        )
    except NameError:
        utilo.error('could not register admin_helpdesk')
    # talker
    if viewo.config.TALKER:
        import viewo_talk
        viewo_talk.register_talkme(appi, prefix=viewo.config.API_PREFIX)
    # configure user access manager
    viewo.user.loginmanager.create_loginmanager(appi)
    # ensure that paths are created
    appi.before_first_request(viewo.path.init)
    # track every user request
    appi.before_request(viewo.tracking.before_each_request)
    # start finding provider
    viewo.api_.findings.data.start()
    # return configured app instance
    return appi


def configure(appi, config):
    """Set environment for application. Decide between test environment and
    production environment

    Args:
        appi(Flask): application to configure, which holds config
        config(dict): vars to export as global environment
    """
    cache = 'NullCache'
    if config is None:
        cache = viewo.cache.TYPE
        # Production environment
        # load the instance config, if it exists
        common_, todo_, ready_ = configos.environment()
        appi.config['COMMON'] = common_
        appi.config['TODO'] = todo_
        appi.config['READY'] = ready_
        try:
            appi.config[admin_helpdesk.ADMIN_HELPDESK] = os.environ[admin_helpdesk.ADMIN_HELPDESK]  # yapf:disable
        except NameError:
            # TODO look here later
            pass
    else:
        # Test environment
        # load the test config if passed in
        appi.config.update(config)
    # setup cache
    viewo.cache.CACHE.init_app(
        appi,
        config=dict(
            CACHE_TYPE=cache,
            CACHE_NO_NULL_WARNING=True,
        ),
    )


def init_error_handler(app: flask.Flask):  # pylint:disable=W0621
    """Add errorhandler for unresolved resources

    Args:
        app(Flask): app to add errorhandler
    """

    @app.errorhandler(404)
    def not_found(_):  # pylint:disable=W0612,W0613
        error = flask.render_template(
            'public/error.html',
            errorpage='Die Seite',
        )
        return error
