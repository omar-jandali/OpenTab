# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0024_auto_20170730_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='funding',
            field=models.DecimalField(default=0.0, max_digits=9, decimal_places=2),
        ),
    ]
