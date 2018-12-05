from django.forms import *
from django.db.models import Q
from django import forms
from django.forms import extras, Widget
from .models import *

VIEWLOGGER_REQUEST_TYPE = (('', "Select"), ("POST", "POST"), ("GET", "GET"))


class ViewLogger_Form(forms.Form):
    request_method = forms.ChoiceField(choices=VIEWLOGGER_REQUEST_TYPE,
                                       label="Request Method",
                                       initial='',
                                       required=False,
                                       widget=forms.Select(attrs={"class": "form-control"}))
    url = forms.CharField(label="URL", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    done_by = forms.CharField(label="Done By", required=False,
                              widget=forms.TextInput(attrs={'class': "form-control"}))
    done_on = forms.DateTimeField(label="Done On",
                                  widget=forms.widgets.DateInput(
                                      attrs={'class': 'form-control datePicker', 'type': 'date'}),
                                  required=False)

    def __init__(self, *args, **kwargs):
        views = kwargs.pop('views',None)
        super(ViewLogger_Form, self).__init__(*args, **kwargs)
        if views:
            views.insert(0, ("","Select"))
            self.fields['view_name'] = forms.ChoiceField(choices=views,
                                                         label="View Name",
                                                         initial='',
                                                         required=False,
                                                         widget=forms.Select(attrs={"class": "form-control"}))
        else:
            self.fields['view_name'] = forms.CharField(label="View Name", required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = Log
        fields = ('view_name', 'request_method', 'url', 'done_by','done_on')