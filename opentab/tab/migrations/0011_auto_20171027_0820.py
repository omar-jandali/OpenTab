# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 08:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0010_auto_20171027_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='accepted',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='useractivity',
            name='expense',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tab.Expense'),
        ),
    ]