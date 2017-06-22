# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0006_auto_20170620_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='group_reference',
            field=models.IntegerField(default=0),
        ),
    ]
