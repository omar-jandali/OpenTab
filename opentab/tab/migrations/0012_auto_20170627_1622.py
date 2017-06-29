# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0011_auto_20170625_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='group',
            field=models.ForeignKey(default=1, to='tab.Group'),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
