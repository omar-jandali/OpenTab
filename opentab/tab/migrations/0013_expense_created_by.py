# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0012_auto_20171028_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='created_by',
            field=models.CharField(default='username', max_length=200),
        ),
    ]
