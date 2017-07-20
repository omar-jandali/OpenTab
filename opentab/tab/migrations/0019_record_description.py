# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0018_auto_20170710_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='description',
            field=models.CharField(max_length=20, default='group expense'),
        ),
    ]
