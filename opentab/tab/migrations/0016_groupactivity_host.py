# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0015_useractivity_validation'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupactivity',
            name='host',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
