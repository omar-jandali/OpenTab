from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

FRIEND_CATEGORY_CHOICES = (
    ('1', 'default'),
    ('2', 'friend'),
    ('3', 'family'),
    ('4', 'favorite'),
)

FRIEND_STATUS_CHOICES = (
    ('1', 'default'),
    ('2', 'blocked'),
)

GROUP_STATUS_CHOICES = (
    ('1', 'active'),
    ('2', 'didabled'),
    ('3', 'suspended'),
)

MEMBER_STATUS_CHOICES = (
    ('1', 'member'),
    ('2', 'host'),
)

RECORD_SPLIT_CHOICES = (
    ('1', 'even'),
    ('2', 'individual'),
)

RECORD_STATUS_CHOICES = (
    ('1', 'unverified'),
    ('2', 'verified'),
)

NOTIFICATION_TYPE_CHOICES = (
    ('0', 'group'),
    ('1', 'record'),
    ('2', 'request'),
    ('3', 'friend'),
)

class Request(models.Model):
    user = models.CharField(max_length=22, default='current user')
    requested = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):
    user = models.CharField(max_length=22, default='current user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    category = models.SmallIntegerField(choices=FRIEND_CATEGORY_CHOICES, default=1)
    status = models.SmallIntegerField(choices=FRIEND_STATUS_CHOICES, default=1)
    created = models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    name = models.CharField(max_length = 25)
    description = models.CharField(max_length = 250)
    count = models.SmallIntegerField(default=1)
    status = models.SmallIntegerField(choices=GROUP_STATUS_CHOICES, default=1)
    reference_code = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) #user
    group = models.ForeignKey(Group, default=1 , on_delete=models.CASCADE) #user
    status = models.SmallIntegerField(choices=MEMBER_STATUS_CHOICES, default=1) #user
    created = models.DateTimeField(auto_now_add=True) #server

class Record(models.Model):
    split = models.SmallIntegerField(choices=RECORD_SPLIT_CHOICES, default=1) #user
    status = models.SmallIntegerField(choices=RECORD_STATUS_CHOICES, default=1) #server
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE) #server
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) #server
    created = models.DateTimeField(auto_now_add=True) #server

class Transaction(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=9,default=0.00)
    description = models.CharField(max_length=250)
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    group = models.ForeignKey(Group, on_delete=models.CASCADE) #server
    description = models.CharField(max_length=200) #server
    created = models.DateTimeField(auto_now_add=True) #server

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    description = models.CharField(max_length=200)  # server
    seen = models.BooleanField()  # server
    types = models.SmallIntegerField(choices=NOTIFICATION_TYPE_CHOICES, default=1)  # server
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
