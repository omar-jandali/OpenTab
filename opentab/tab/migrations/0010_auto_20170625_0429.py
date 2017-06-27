# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0009_auto_20170624_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='group_reference',
        ),
        migrations.RemoveField(
            model_name='record',
            name='group_reference',
        ),
        migrations.AddField(
            model_name='member',
            name='group',
            field=models.ForeignKey(default=1, to='tab.Group'),
        ),
        migrations.AlterField(
            model_name='group',
            name='created_by',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.CharField(max_length=25),
        ),
    ]
