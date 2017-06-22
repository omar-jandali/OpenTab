# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0003_auto_20170620_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='reference_code',
            field=models.IntegerField(default=0),
        ),
    ]
