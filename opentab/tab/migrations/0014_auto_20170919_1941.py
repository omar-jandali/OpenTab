# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 19:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0013_dwolla'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dwolla',
            old_name='funding_source',
            new_name='source_id',
        ),
        migrations.RenameField(
            model_name='dwolla',
            old_name='customer_id',
            new_name='source_name',
        ),
    ]
