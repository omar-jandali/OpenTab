# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0020_auto_20170711_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='privacy',
            field=models.SmallIntegerField(default=1),
        ),
    ]
