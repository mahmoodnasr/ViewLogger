# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ViewLogger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='duration',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='response_status',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
