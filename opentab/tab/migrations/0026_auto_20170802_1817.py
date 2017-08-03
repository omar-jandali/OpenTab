# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0025_member_funding'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='category',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='activity',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='activity',
            name='group',
            field=models.ForeignKey(null=True, to='tab.Group'),
        ),
    ]
