# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=250)),
                ('group_image', models.ImageField(upload_to='')),
                ('levels', models.SmallIntegerField()),
                ('status', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='tab.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=200)),
                ('status', models.SmallIntegerField()),
                ('type', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('pic', models.ImageField(upload_to='')),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=45)),
                ('phone', models.BigIntegerField()),
                ('dob', models.DateField()),
                ('status', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('amount', models.DecimalField(max_digits=2, decimal_places=2)),
                ('description', models.CharField(max_length=200)),
                ('status', models.SmallIntegerField()),
                ('type', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='tab.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='group',
            field=models.ForeignKey(to='tab.Group'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
