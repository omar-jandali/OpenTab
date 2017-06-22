# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0002_remove_group_group_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='type',
            new_name='status',
        ),
        migrations.RemoveField(
            model_name='group',
            name='levels',
        ),
        migrations.AddField(
            model_name='group',
            name='count',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
    ]
