# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0004_group_reference_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='group',
            new_name='group_reference',
        ),
    ]
