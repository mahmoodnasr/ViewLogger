import time,json,sys
from datetime import datetime

from django.conf import settings as conf_settings
from django.shortcuts import HttpResponse

from .models import Log

Object = object
if sys.version_info >= (3, 0, 0):
    from django.utils.deprecation import MiddlewareMixin

    Object = MiddlewareMixin


class ViewLoggerMiddleware(Object):

    def process_exception(self, request, exception):
        log = request.view_logger_obj
        log.request_body = {"error":exception.args}
        log.save()
        html = """
        <h3>An unexpected error occurred.</h3>
            <p>Something went seriously wrong, the admins have been notified and they will fix it as fast as they can.
                Sorry for the inconvenience. <button onclick="goBack()">Go Back</button>  </p>
                <script> function goBack() { window.history.back(); } </script>
        """
        return HttpResponse(html, content_type="text/html")

    def process_response(self, request, response):
        try:
            log = request.view_logger_obj
            now = time.time()
            duration = now - request.start_time
            log.duration = "{0:.5f}".format(duration)
            log.response_status = response.status_code
            log.save()
        except:
            pass
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        maxColumnSize = 10
        username = request.user.username if request.user else "None"
        body_data = request.GET if request.method == 'GET' else request.POST
        try:
            view = view_func.func_name
        except:
            view = view_func.__name__
        view = view_func.__name__
        path = request.META["PATH_INFO"]
        VIEWLOGGER_METHODS = [i.lower() for i in getattr(conf_settings, "VIEWLOGGER_METHODS", ['post', 'get'])]
        EXEMPTED_VIEWS = getattr(conf_settings, 'VIEWLOGGER_EXEMPTED_VIEWS', ("",))
        EXEMPTED_PARAMETER = getattr(conf_settings, 'VIEWLOGGER_EXEMPTED_PARAMETER')
        EXEMPTED_PATHS = getattr(conf_settings, 'VIEWLOGGER_EXEMPTED_PATHS', ("",))
        if not path in EXEMPTED_PATHS and not view in EXEMPTED_VIEWS and request.method.lower() in VIEWLOGGER_METHODS:
            log = Log()
            requestBody = {}
            if EXEMPTED_PARAMETER:
                for item in body_data:
                    if item not in EXEMPTED_PARAMETER:
                        requestBody[item] = body_data[item]
                    else:
                        requestBody[item] = len(body_data[item]) * "*" if len(
                            body_data[item]) < maxColumnSize else maxColumnSize * "*" + (5 * ".")
            else:
                requestBody = body_data
            method = request.method.upper()
            log.request_body = requestBody
            log.url = request.get_full_path().split("?")[0] if method == "GET" else request.get_full_path()
            log.view_name = view
            log.done_by = username
            log.done_on = datetime.now()
            log.view_kwargs = view_kwargs
            log.view_args = view_args
            log.request_method = method
            log.save()
            request.view_logger_obj = log
            request.start_time = time.time()
