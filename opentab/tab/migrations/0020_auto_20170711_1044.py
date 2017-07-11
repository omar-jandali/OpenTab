# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0019_record_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='privacy',
            field=models.SmallIntegerField(default=1, choices=[('1', 'public'), ('2', 'private')]),
        ),
    ]
