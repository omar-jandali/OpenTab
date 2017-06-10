from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.SmallIntegerField()
    type = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    name = models.CharField(max_length=45)
    status = models.SmallIntegerField()
    type = models.SmallIntegerField()
    balance = models.DecimalField(decimal_places=2)
    member_count = models.SmallIntegerField()
    created_by = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    type = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    user1 = models.ForeignKey(User)
    user2 = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


class Record(models.Model):
    amount = models.DecimalField(decimal_places=2)
    description = models.models.CharField(max_length=200)
    status = models.SmallIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.models.CharField(max_length=200)
    status = models.SmallIntegerField()
    type = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.ImageField()  # Update with options
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    phone = models.BigIntegerField()
    dob = models.DateField()
    status = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
