# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0017_auto_20170702_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pic',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='public',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='privacy',
            field=models.SmallIntegerField(default=1, choices=[('2', 'private'), ('1', 'public')]),
        ),
        migrations.AlterField(
            model_name='notification',
            name='category',
            field=models.SmallIntegerField(default=1, choices=[('1', 'group'), ('2', 'record'), ('3', 'request'), ('4', 'friend')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
