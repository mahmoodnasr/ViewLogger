import time
from datetime import datetime
from .models import Log
from django.conf import settings as conf_settings
import sys
Object = object
if sys.version_info >= (3,0,0):
    from django.utils.deprecation import MiddlewareMixin
    Object = MiddlewareMixin

class ViewLoggerMiddleware(Object):

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
        if getattr(conf_settings, "VIEWLOGGER_SAVE_DURATION", False) and not "ViewLoggerStart" in request.session:
            request.session["ViewLoggerStart"] = getattr(time,"time_ns",time.time)()
            return
        VIEWLOGGER_METHODS = [i.lower() for i in  getattr(conf_settings, "VIEWLOGGER_METHODS",['post','get'])]
        EXEMPTED_VIEWS = getattr(conf_settings, 'VIEWLOGGER_EXEMPTED_VIEWS', ("",))
        EXEMPTED_PARAMETER = getattr(conf_settings,'VIEWLOGGER_EXEMPTED_PARAMETER')
        EXEMPTED_PATHS = getattr(conf_settings, 'VIEWLOGGER_EXEMPTED_PATHS', ("",))
        if not path in EXEMPTED_PATHS and not view in EXEMPTED_VIEWS and request.method.lower() in VIEWLOGGER_METHODS:
            log = Log()
            requestBody = {}
            if EXEMPTED_PARAMETER:
                for item in body_data:
                    if item not in EXEMPTED_PARAMETER:
                        requestBody[item] = body_data[item]
                    else:
                        requestBody[item] = len(body_data[item]) * "*" if len(body_data[item]) < maxColumnSize else maxColumnSize * "*" + (5 * ".")
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
            now = getattr(time,"time_ns",time.time)()
            d = (now - request.session.pop("ViewLoggerStart",now))
            log.duration = "{0:.3f}".format(d)
            print now,request.session.get("ViewLoggerStart"), log.duration
            log.save()
