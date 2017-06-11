from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE) #server
    user2 = models.ForeignKey(User, on_delete=models.CASCADE) #server
    status = models.SmallIntegerField() #server
    # 0 = friend *default*
    # 1 = family
    # 2 = favorite
    type = models.SmallIntegerField() #server
    # 0 = default [active]
    # 1 = blocked
    created = models.DateTimeField(auto_now_add=True) #server


class Group(models.Model):
    name = models.CharField(max_length=45) #user
    status = models.SmallIntegerField() #server
    # 0 = active
    # 1 = non active
    # 2 = deactive
    type = models.SmallIntegerField() #user
    # 0 = basic[1 - 5 people]
    # 1 = bronze[5 - 7 people]
    # 2 = silver[8 - 10 people]
    # 3 = gold[11 - 13 people]
    # 4 = platnium[14+]
    balance = models.DecimalField(decimal_places=2) #server
    # default = 0.00
    #   if the group is a paid group, the defult will be = -#.##
    member_count = models.SmallIntegerField() #user
    created_by = models.ForeignKey(User) #server
    created = models.DateTimeField(auto_now_add=True) #server


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user
    group = models.ForeignKey(Group, on_delete=models.CASCADE) #server
    type = models.SmallIntegerField() #user
    # 0 = member
    # 1 = host
    created = models.DateTimeField(auto_now_add=True) #server


class Request(models.Model):
    user1 = models.ForeignKey(User) #server
    user2 = models.ForeignKey(User) #user
    created = models.DateTimeField(auto_now_add=True) #server


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    group = models.ForeignKey(Group, on_delete=models.CASCADE) #server
    description = models.models.CharField(max_length=200) #server
    created = models.DateTimeField(auto_now_add=True) #server


class Record(models.Model):
    amount = models.DecimalField(decimal_places=2) #user
    description = models.models.CharField(max_length=200) #user
    status = models.SmallIntegerField() #server
    # 0 = unverified
    # 1 = verified
    ### I added a type for the Record which will determine if the bill is an
    ### even split between everyone selected or indiviual amounts
    type = models.SmallIntegerField() #user
    # 0 = even split
    # 1 = individual split
    group = models.ForeignKey(Group, on_delete=models.CASCADE) #server
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    created = models.DateTimeField(auto_now_add=True) #server


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    description = models.models.CharField(max_length=200) #server
    status = models.SmallIntegerField() # server
    # 0 = unseen
    # 1 = seen
    type = models.SmallIntegerField() #server
    # 0 = group
    # 1 = Record
    # 3 = Request
    # 4 = friend
    created = models.DateTimeField(auto_now_add=True) #server


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    pic = models.ImageField()  # Update with options
    city = models.CharField(max_length=45) #user
    state = models.CharField(max_length=45) #user
    phone = models.BigIntegerField() #user
    dob = models.DateField() #user
    status = models.SmallIntegerField() #user
    # 0 = public
    # 1 = private
    created = models.DateTimeField(auto_now_add=True) #server
