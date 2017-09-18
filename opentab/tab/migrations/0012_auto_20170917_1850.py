# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0011_auto_20170914_0351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='synapse_id',
        ),
        migrations.AddField(
            model_name='profile',
            name='dwolla_id',
            field=models.CharField(default='https://api-sandbox.dwolla.com', max_length=200),
        ),
    ]
