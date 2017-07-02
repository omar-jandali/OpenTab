# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tab', '0015_auto_20170629_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('user', models.CharField(max_length=22, default='current user')),
                ('category', models.SmallIntegerField(default=1, choices=[('1', 'default'), ('2', 'friend'), ('3', 'family'), ('4', 'favorite')])),
                ('status', models.SmallIntegerField(default=1, choices=[('1', 'default'), ('2', 'blocked')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('friend', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('user', models.CharField(max_length=22, default='current user')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('requested', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='notification',
            name='type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
        migrations.AddField(
            model_name='notification',
            name='category',
            field=models.SmallIntegerField(default=1, choices=[('0', 'group'), ('1', 'record'), ('2', 'request'), ('3', 'friend')]),
        ),
        migrations.AddField(
            model_name='profile',
            name='public',
            field=models.SmallIntegerField(default=1, choices=[('2', 'private'), ('1', 'public')]),
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'active'), ('2', 'didabled'), ('3', 'suspended')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'member'), ('2', 'host')]),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('2', 'read'), ('1', 'unread')]),
        ),
        migrations.AlterField(
            model_name='record',
            name='split',
            field=models.SmallIntegerField(default=1, choices=[('1', 'even'), ('2', 'individual'), ('3', 'asdfasfd')]),
        ),
        migrations.AlterField(
            model_name='record',
            name='status',
            field=models.SmallIntegerField(default=1, choices=[('1', 'unverified'), ('2', 'verified')]),
        ),
    ]
