# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0016_auto_20170701_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='group',
            name='member_count',
        ),
        migrations.RemoveField(
            model_name='group',
            name='type',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='seen',
        ),
        migrations.RemoveField(
            model_name='record',
            name='even_split',
        ),
        migrations.RemoveField(
            model_name='record',
            name='verified',
        ),
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('2', 'read'), ('1', 'unread')]),
        ),
        migrations.AddField(
            model_name='record',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='record',
            name='split',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='record',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'unverified'), ('2', 'verified')]),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='profile',
            name='public',
            field=models.SmallIntegerField(default=1, choices=[('1', 'public'), ('2', 'private')]),
        ),
    ]
