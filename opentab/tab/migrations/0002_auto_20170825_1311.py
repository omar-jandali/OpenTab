# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tab', '0001_initial'),
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
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('amount', models.DecimalField(default=0.0, max_digits=9, decimal_places=2)),
                ('description', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('memo', models.CharField(max_length=200, default='money transfer')),
                ('transfer', models.SmallIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='friend',
            name='type',
        ),
        migrations.RemoveField(
            model_name='group',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='group',
            name='member_count',
        ),
        migrations.RemoveField(
            model_name='group',
            name='type',
        ),
        migrations.RemoveField(
            model_name='member',
            name='type',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='seen',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pic',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='public',
        ),
        migrations.RemoveField(
            model_name='record',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='record',
            name='even_split',
        ),
        migrations.RemoveField(
            model_name='record',
            name='verified',
        ),
        migrations.RemoveField(
            model_name='request',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='request',
            name='user2',
        ),
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
        migrations.AddField(
            model_name='friend',
            name='category',
            field=models.SmallIntegerField(default=1, choices=[('1', 'default'), ('2', 'friend'), ('3', 'family'), ('4', 'favorite')]),
        ),
        migrations.AddField(
            model_name='group',
            name='count',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='reference_code',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='funding',
            field=models.DecimalField(default=0.0, max_digits=9, decimal_places=2),
        ),
        migrations.AddField(
            model_name='member',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'member'), ('2', 'host')]),
        ),
        migrations.AddField(
            model_name='notification',
            name='category',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='dob_day',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='dob_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='dob_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=25, default='first'),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=25, default='last'),
        ),
        migrations.AddField(
            model_name='profile',
            name='privacy',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='record',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='record',
            name='split',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='record',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'unverified'), ('2', 'verified')]),
        ),
        migrations.AddField(
            model_name='request',
            name='requested',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.CharField(max_length=22, default='current user'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='group',
            field=models.ForeignKey(null=True, to='tab.Group'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friend',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friend',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'default'), ('2', 'blocked')]),
        ),
        migrations.AlterField(
            model_name='friend',
            name='user',
            field=models.CharField(max_length=22, default='current user'),
        ),
        migrations.AlterField(
            model_name='group',
            name='created_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'active'), ('2', 'didabled'), ('3', 'suspended')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='group',
            field=models.ForeignKey(default=1, to='tab.Group'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(max_length=25, default='state'),
        ),
        migrations.AlterField(
            model_name='record',
            name='description',
            field=models.CharField(max_length=20, default='group expense'),
        ),
        migrations.AlterField(
            model_name='record',
            name='group',
            field=models.ForeignKey(default=1, to='tab.Group'),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='group',
            field=models.ForeignKey(default=1, to='tab.Group'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='record',
            field=models.ForeignKey(default=1, to='tab.Record'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupbalance',
            name='group',
            field=models.ForeignKey(to='tab.Group'),
        ),
        migrations.AddField(
            model_name='groupbalance',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
