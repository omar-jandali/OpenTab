# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0007_auto_20170621_0003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='type',
            new_name='split',
        ),
    ]
