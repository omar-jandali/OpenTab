# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tab', '0002_auto_20170825_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('from_acct', models.CharField(max_length=150, default='account')),
                ('to_acct', models.CharField(max_length=150, default='accont')),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('memo', models.CharField(max_length=200, default='memo')),
                ('frequency', models.SmallIntegerField(default=1)),
                ('status', models.SmallIntegerField(default=1)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
