# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0004_accounts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfers',
            old_name='from_acct',
            new_name='main',
        ),
        migrations.RenameField(
            model_name='transfers',
            old_name='to_acct',
            new_name='transfer',
        ),
    ]
