# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0022_auto_20170727_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbalance',
            name='memo',
            field=models.CharField(max_length=200, default='money transfer'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('2', 'read'), ('1', 'unread')]),
        ),
    ]
