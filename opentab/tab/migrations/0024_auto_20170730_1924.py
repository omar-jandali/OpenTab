# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tab', '0023_auto_20170727_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupBalance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('memo', models.CharField(max_length=200, default='group transfer')),
                ('transfer', models.SmallIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='tab.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='userbalance',
            old_name='activity',
            new_name='transfer',
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'unread'), ('2', 'read')]),
        ),
    ]
