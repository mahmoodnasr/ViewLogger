import django_tables2 as tables
from .models import *
from django.utils.safestring import mark_safe


class ViewLoggor_Data(tables.Table):
    id = tables.Column(verbose_name="#")
    url = tables.Column(verbose_name="URL")
    view_args = tables.TemplateColumn("NA", verbose_name="View Args")
    view_kwargs = tables.TemplateColumn("NA", verbose_name="View Kwargs")
    request_method = tables.Column(verbose_name="Request Method")
    request_body = tables.TemplateColumn("NA", verbose_name="Request Body")
    by = tables.Column(verbose_name="Done By")
    event_time = tables.DateColumn(verbose_name="Done On")

    def render_request_body(self, value, record):
        res = ""
        for k, v in record['request_body'].items():
            res += k + " : " + v + "\n"
        return mark_safe(res)

    def render_view_args(self, value, record):
        res = ""
        for v in record['view_args']:
            res += v + "\n"
        return mark_safe(res)

    def render_view_kwargs(self, value, record):
        res = ""
        for k, v in record['view_kwargs'].items():
            res += k + " : " + v + "\n"
        return mark_safe(res)

    class Meta:
        model = Log
        attrs = {"class": "paleblue"}
        fields = ['id', 'url', 'view_args', 'view_kwargs',
                  'request_method', 'request_body', 'by', 'event_time']
