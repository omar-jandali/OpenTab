# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0005_auto_20171018_0703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='group_ref',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='status',
        ),
        migrations.AddField(
            model_name='expense',
            name='location',
            field=models.CharField(default='location', max_length=100),
        ),
    ]