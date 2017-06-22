# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0005_auto_20170620_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
    ]
