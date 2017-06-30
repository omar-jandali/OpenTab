# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0014_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='record',
            name='description',
        ),
    ]
