from datetime import datetime
from ViewLogger.models import Log
from django.conf import settings as conf_settings


class ViewLoggerMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        username = request.user.username if request.user else "None"
        body_data = request.GET if request.method == 'GET' else request.POST
        view = view_func.func_name
        path = request.META["PATH_INFO"]

        VIEWLOGGER_METHODS = [i.lower() for i in conf_settings.VIEWLOGGER_METHODS] if  hasattr(conf_settings, "VIEWLOGGER_METHODS") else ['post','get']
        EXEMPTED_VIEWS = conf_settings.VIEWLOGGER_EXEMPTED_VIEWS if hasattr(conf_settings, 'VIEWLOGGER_EXEMPTED_VIEWS') else ("")
        EXEMPTED_PATHS = conf_settings.VIEWLOGGER_EXEMPTED_PATHS if hasattr(conf_settings, 'VIEWLOGGER_EXEMPTED_PATHS') else ("")
        if not path in EXEMPTED_PATHS and not view in EXEMPTED_VIEWS and request.method.lower() in VIEWLOGGER_METHODS:
            log = Log()
            log.request_body = body_data
            log.url = request.get_full_path()
            log.view_name = view
            log.done_by = username
            log.done_on = datetime.now()
            log.view_kwargs = view_kwargs
            log.view_args = view_args
            log.request_method = request.method.upper()
            log.save()
