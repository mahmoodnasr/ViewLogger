# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ViewLogger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='duration',
            field=models.DecimalField(default=0, null=True, max_digits=5, decimal_places=5),
        ),
    ]
