from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length = 25)
    description = models.CharField(max_length = 250)
    #group_image = models.ImageField()
    count = models.SmallIntegerField(default=1)
    # the count above will keep track of the number of members that are in the
    # group at all times.
    status = models.SmallIntegerField(default=1)
    # 1 active
    # 2 deactive
    # 3 suspended
    reference_code = models.IntegerField(default=0)
    # the following is going to be a code that is created by the server that will
    # be used by all other parts of the appFication in order to keep track of each
    # group that is created. It will be unique for every different group.
    created_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) #user
    group = models.ForeignKey(Group, default=1 , on_delete=models.CASCADE) #user
    status = models.SmallIntegerField(default=1) #user
    # 1 = member
    # 2 = host
    created = models.DateTimeField(auto_now_add=True) #server

class Record(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0.00) #user
    description = models.CharField(max_length=250) #user
    status = models.SmallIntegerField(default=1) #server
    # 1 = unverified
    # 2 = verified
    split = models.SmallIntegerField(default=1) #user
    # added a type for the Record which will determine if the bill is an
    # even split between everyone selected or indiviual amounts
    # 1 = even split
    # 2 = individual split
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE) #server
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) #server
    created = models.DateTimeField(auto_now_add=True) #server

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    group = models.ForeignKey(Group, on_delete=models.CASCADE) #server
    description = models.CharField(max_length=200) #server
    created = models.DateTimeField(auto_now_add=True) #server




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    description = models.CharField(max_length=200) #server
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
