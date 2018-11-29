from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
import datetime
from .forms import *
# from .tables import *
# from django_tables2.export.export import TableExport
from django.http import HttpResponse


def mainViewLogger(request):
    res = {}
    views = [(s['view_name'], s['view_name']) for s in Log.objects.values("view_name").distinct().order_by("view_name")]
    if request.method == "GET":
        res["form"] = ViewLogger_Form(views=views)
        # export_format = request.GET.get('_export', None)
        # if export_format and TableExport.is_valid_format(export_format):
        #     data = fetchChanges(request)
        #     table = ViewLoggor_Data(data['changes'])
        #     exporter = TableExport(export_format, table)
        #     return exporter.response('ViewLogger_Data.%s' % (export_format))
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
            request.kwargs = kwargs
            request.args = args
            res = fetchChanges(request)
            res['form'] = form
            if "export" in request.POST:
                template = 'ViewLogger_Data.html'
                return reportAsExcel(request, template, res['changes'])
            return render_to_response("mainLog.html", res, context_instance=RequestContext(request))
        else:
            print form.errors


def fetchChanges(request):
    k = request.kwargs
    a = request.args
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
        # if 'csrfmiddlewaretoken' in change.request_body: del change.request_body['csrfmiddlewaretoken']
        reqBody = {}
        if change.request_body:
            for k in change.request_body:
                if len(change.request_body[k]) > 0: reqBody[k] = change.request_body[k]
        row['request_body'] = reqBody
        row['request_method'] = change.request_method
        rows.append(row)
    count = len(rows)
    res = {"count": count, "changes": rows}
    return res


def reportAsExcel(request, temp, vars):
    import csv
    response = HttpResponse(content_type='text/csv, application/octet-stream')
    response["Content-Disposition"] = "attachment; filename='{}'".format(temp.replace(".html", ".xls"))
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow(['', '', '','ViewLogger Data'])
    writer.writerow(['', '', '', '', '', '', '', '',])
    names = ['#', 'URL','View Args','View Kwargs','Request Method','Request Body','Done By','Done On']
    writer.writerow(names)
    for obj in vars:
        temp_list = []
        temp_list.append(obj['id'])
        temp_list.append(obj['url'])
        res = ""
        for k in obj['view_args']:res += k + "\n"
        temp_list.append(res)
        res = ""
        for k, v in obj['view_kwargs'].items():res += k + " : " + v + "\n"
        temp_list.append(res)
        temp_list.append(obj['request_method'])
        res = ""
        for k, v in obj['request_body'].items():res+=k+" : "+v+"\n"
        temp_list.append(res)
        temp_list.append(obj['name'])
        temp_list.append(obj['event_time'])
        writer.writerow(temp_list)
    return response