# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
try:
    from django.db.models import JSONField
except ImportError:
    try:
        from jsonfield.fields import JSONField
    except ImportError:
        raise ImportError("Can't find a JSONField implementation, please install jsonfield if django < 4.0")


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
                ('request_body', JSONField(default=dict)),
                ('url', models.CharField(max_length=255)),
                ('view_args', JSONField(default=list)),
                ('view_kwargs', JSONField(default=dict)),
                ('done_by', models.CharField(max_length=255)),
                ('done_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
