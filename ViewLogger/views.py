from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
import datetime
from .forms import *


def mainViewLogger(request):
    res = {}
    views = [(s['view_name'], s['view_name']) for s in Log.objects.values("view_name").distinct()]
    if request.method == "GET":
        res["form"] = ViewLogger_Form(views=views)
        res.update(csrf(request))
        return render_to_response("mainLog.html", res, context_instance=RequestContext(request))
    if request.method == "POST":
        form = ViewLogger_Form(request.POST, views=views)
        if form.is_valid():
            view_name = form.cleaned_data.get('view_name')
            request_method = form.cleaned_data.get('request_method')
            url = form.cleaned_data.get('url')
            done_by = form.cleaned_data.get('done_by')
            done_on = form.cleaned_data.get('done_on', None)
            kwargs = {}
            args = []
            if view_name != '': kwargs['view_name'] = view_name
            if request_method != '': kwargs['request_method'] = request_method
            if url != '': kwargs['url__contains'] = url
            if done_by != '': kwargs['done_by'] = done_by
            if done_on is not None:
                args = (Q(done_on__lt=datetime.datetime(done_on.year, done_on.month, done_on.day + 1)),
                        Q(done_on__gte=datetime.datetime(done_on.year, done_on.month, done_on.day)),)
            request.session['kwargs'] = kwargs
            request.session['args'] = args
            res = fetchChanges(request)
            res['form'] = form
            return render_to_response("mainLog.html", res, context_instance=RequestContext(request))
        else:
            print form.errors


def fetchChanges(request):
    k = request.session['kwargs']
    a = request.session['args']
    changes = Log.objects.filter(*a, **k).order_by("-id")
    rows = []
    for change in changes:
        row = {}
        row["event_time"] = change.done_on
        row["by"] = change.done_by
        row["name"] = change.view_name
        row["id"] = change.id
        row['url'] = change.url
        row['view_args'] = change.view_args
        row['view_kwargs'] = change.view_kwargs
        if 'csrfmiddlewaretoken' in change.request_body: del change.request_body['csrfmiddlewaretoken']
        reqBody = {}
        for k in change.request_body:
            if len(change.request_body[k]) > 0 : reqBody[k] = change.request_body[k]
        row['request_body'] = reqBody
        row['request_method'] = change.request_method
        rows.append(row)
    count = len(rows)
    res = {"count": count, "changes": rows}
    return res
