from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    STATUS_CHOICES = (
        ('0', 'friend'),
        ('1', 'family'),
        ('2', 'favorite'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')  # server
    TYPE_CHOICES = (
        ('0', 'default'),
        ('1', 'blocked'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='0')  # server
    created = models.DateTimeField(auto_now_add=True)  # server


class Group(models.Model):
    name = models.CharField(max_length=45)  # user
    STATUS_CHOICES = (
        ('0', 'active'),
        ('1', 'non_active'),
        ('2', 'deactive'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')  # server
    TYPE_CHOICES = (
        ('0', 'basic'),
        ('1', 'bronze'),
        ('2', 'silver'),
        ('3', 'gold'),
        ('4', 'platnium'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='0')  # user
    # 0 = basic[1 - 5 people]
    # 1 = bronze[5 - 7 people]
    # 2 = silver[8 - 10 people]
    # 3 = gold[11 - 13 people]
    # 4 = platnium[14+]
    balance = models.DecimalField(decimal_places=2, default=0)  # server
    member_count = models.SmallIntegerField()  # user
    created_by = models.ForeignKey(User)  # server
    created = models.DateTimeField(auto_now_add=True)  # server


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # user
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # server
    TYPE_CHOICES = (
        ('0', 'member'),
        ('1', 'host'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)  # user
    created = models.DateTimeField(auto_now_add=True)  # server


class Request(models.Model):
    user1 = models.ForeignKey(User)  # server
    user2 = models.ForeignKey(User)  # user
    created = models.DateTimeField(auto_now_add=True)  # server


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # server
    description = models.models.CharField(max_length=200)  # server
    created = models.DateTimeField(auto_now_add=True)  # server


class Record(models.Model):
    amount = models.DecimalField(decimal_places=2)  # user
    description = models.models.CharField(max_length=200)  # user
    verified = models.BooleanField()  # server
    even_split = models.BooleanField()  # user
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # server
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    created = models.DateTimeField(auto_now_add=True)  # server


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    description = models.models.CharField(max_length=200)  # server
    seen = models.BooleanField()  # server
    TYPE_CHOICES = (
        ('0', 'group'),
        ('1', 'record'),
        ('2', 'request'),
        ('3', 'friend'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)  # server
    created = models.DateTimeField(auto_now_add=True)  # server


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    pic = models.ImageField()  # Update with options
    city = models.CharField(max_length=45)  # user
    state = models.CharField(max_length=45)  # user
    phone = models.BigIntegerField()  # user
    dob = models.DateField()  # user
    public = models.BooleanField()  # user
    created = models.DateTimeField(auto_now_add=True)  # server
