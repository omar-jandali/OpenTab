# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0008_auto_20170623_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='group',
        ),
        migrations.AddField(
            model_name='record',
            name='group_reference',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='amount',
            field=models.DecimalField(default=0.0, max_digits=9, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='record',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='record',
            name='split',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='record',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
    ]
