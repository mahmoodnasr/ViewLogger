from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
import datetime
from .forms import *
# from .tables import *
# from django_tables2.export.export import TableExport
from django.http import HttpResponse
import os
import commands
from django.conf import settings
from ViewLogger import Common
import json
import re


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
                return reportAsExcel(template, res['changes'])
            return render_to_response("mainLog.html", res, context_instance=RequestContext(request))
        else:
            print form.errors


def fetchChanges(request):
    from .api import fetchChangesAPI
    k = request.kwargs
    a = request.args
    changes = Log.objects.filter(*a, **k).order_by("-id")
    return fetchChangesAPI(changes)


def reportAsExcel(temp, vars,seperated=False):
    import csv
    response = HttpResponse(content_type='text/csv, application/octet-stream')
    response["Content-Disposition"] = "attachment; filename='{}'".format(temp.replace(".html", ".csv"))
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow(['', '', '', 'ViewLogger Data'])
    writer.writerow(['', '', '', '', '', '', '', '', ])
    if seperated:
        for object in vars:
            file = object['file']
            writer.writerow(['File Name = ',file,"",""])
            names = ['#', "View Name", 'URL', 'View Args', 'View Kwargs', 'Request Method', 'Request Body', 'Done By','Done On']
            writer.writerow(names)
            for obj in object['changes']:
                temp_list = []
                temp_list.append("\n".join(obj['id']))
                temp_list.append("\n".join(obj['view_name']))
                temp_list.append("\n".join(obj['url']))
                temp_list.append("\n".join(obj['view_args']))
                temp_list.append("\n".join(obj['view_kwargs']))
                temp_list.append("\n".join(obj['request_method']))
                temp_list.append("\n".join(obj['request_body']))
                temp_list.append("\n".join(obj['done_by']))
                temp_list.append("\n".join(obj['done_by']))
                writer.writerow(temp_list)
    else:
        names = ['#', "View Name", 'URL', 'View Args', 'View Kwargs', 'Request Method', 'Request Body', 'Done By',
                 'Done On']
        writer.writerow(names)
        for obj in vars:
            temp_list = []
            temp_list.append(obj['id'])
            temp_list.append(obj['view_name'])
            temp_list.append(obj['url'])
            res = ""
            for k in obj['view_args']: res += k + "\n"
            temp_list.append(res)
            res = ""
            for k, v in obj['view_kwargs'].items(): res += k + " : " + v + "\n"
            temp_list.append(res)
            temp_list.append(obj['request_method'])
            res = ""
            for k, v in obj['request_body'].items(): res += k + " : " + v + "\n"
            temp_list.append(res)
            temp_list.append(obj['done_by'])
            temp_list.append(obj['done_on'])
            writer.writerow(temp_list)
    return response


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def strSearch(li,bigReg,smallReg):
    tempLi = re.search(bigReg, li)
    if tempLi:
        newLi = str(tempLi.groups())
        temp = re.search(smallReg, newLi)
        result = list(temp.groups())
        newline = re.sub(bigReg,'',li)
        return newline,result if temp else None


def stringToDic(obj):
    rows = []
    lists = obj.split('{  "view_args":')
    for li in lists:
        row = {}
        if li:
            newLi, viewargs = strSearch(li, r'(.*)"view_kwargs"', r'\[(.*?)\]')
            row['view_args'] = viewargs[0].replace('"', '').split(",")
            newLi, viewkwargs = strSearch(newLi, r'(.*)"request_body"', r'\{(.*?)\}')
            row['view_kwargs'] = viewkwargs[0].replace('"', '').split(",")
            newLi, requestbody = strSearch(newLi, r'(.*)"url"', r'\{(.*?)\}')
            row['request_body'] = requestbody[0].replace('"', '').split(",")
            newLi, row['url'] = strSearch(newLi, r'(.*)"done_on"', r': "(.*?)",')
            newLi, row['done_on'] = strSearch(newLi, r'(.*?)"view_name"', r': "(.*?)",')
            newLi, row['view_name'] = strSearch(newLi, r'(.*)"done_by"', r': "(.*?)",')
            newLi, row['done_by'] = strSearch(newLi, r'(.*)"request_method"', r': "(.*?)",')
            newLi, row['request_method'] = strSearch(newLi, r'(.*)"id"', r': "(.*?)",')
            newLi, row['id'] = strSearch(newLi, r'(.*)', ':(.*)\}')
            if row: rows.append(row)
    return rows


def search_in_archives(request):
    res = {}
    dir = settings.VIEWLOGGER_ARCHIVE_DIR if hasattr(settings, 'VIEWLOGGER_ARCHIVE_DIR') else os.path.join(
        settings.BASE_DIR, "ViewLoggerArchive")
    if request.method == "POST":
        form = ViewLogger_Form(request.POST)
        if form.is_valid():
            view_name = form.cleaned_data.get('view_name',None)
            request_method = form.cleaned_data.get('request_method',None)
            url = form.cleaned_data.get('url',None)
            done_by = form.cleaned_data.get('done_by',None)
            done_on = form.cleaned_data.get('done_on', None)
            filesList = [x for x in os.listdir(dir)]
            alloptions = ""
            if url: alloptions += '''|  select(.url | contains("%s")) ''' % (url)
            if view_name: alloptions += '''|  select(.view_name | contains("%s")) ''' % (view_name)
            if done_by: alloptions += '''|  select(.done_by | contains("%s")) ''' % (done_by)
            if done_on: alloptions += '''|  select(.done_on | contains("%s")) ''' % (done_on)
            if request_method: alloptions += '''|  select(.request_method | contains("%s")) ''' % (request_method)

            bin = '%s/ViewLogger/bin/jq-linux64' % (settings.BASE_DIR)
            if not is_exe(bin):
                stat, output = commands.getstatusoutput('chmod +x %s') % (bin)
            objects = []
            for file in filesList:
                print "File = ", file
                cmd = """%s/ViewLogger/bin/jq-linux64 '.[] %s' %s""" % (
                    settings.BASE_DIR, alloptions, dir + "/" + file)
                com = Common.run(cmd,True).replace('\n','')
                if com:
                    objects.append({"file": file, "changes": stringToDic(com)})
            res["objects"] = objects
            res['count'] = len(objects)
            res['form'] = form
            if "export" in request.POST:
                template = 'ViewLogger_Data.html'
                return reportAsExcel(template, res["objects"],True)
            return render_to_response("searchInViewLogger.html", res, context_instance=RequestContext(request))
    if request.method == "GET":
        res["form"] = ViewLogger_Form()
        res.update(csrf(request))
        return render_to_response("searchInViewLogger.html", res, context_instance=RequestContext(request))