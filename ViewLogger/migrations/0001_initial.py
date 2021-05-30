# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('view_name', models.CharField(max_length=255)),
                ('request_method', models.CharField(max_length=5)),
                ('request_body', jsonfield.fields.JSONField(default={})),
                ('url', models.CharField(max_length=255)),
                ('view_args', jsonfield.fields.JSONField(default=[])),
                ('view_kwargs', jsonfield.fields.JSONField(default={})),
                ('done_by', models.CharField(max_length=255)),
                ('done_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
