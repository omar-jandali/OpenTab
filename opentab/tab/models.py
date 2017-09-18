from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# the following is what gives the states to select from when it comes to the states
# field in the model
from django_localflavor_us.models import USStateField

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

RECORD_STATUS_CHOICES = (
    ('1', 'unverified'),
    ('2', 'verified'),
)

NOTIFICATION_CATEGORY_CHOICES = (
    ('1', 'group'),
    ('2', 'record'),
    ('3', 'request'),
    ('4', 'friend'),
)

NOTIFICATION_STATUS_CHOICES = {
    ('1', 'unread'),
    ('2', 'read'),
}

PROFILE_PRIVACY_CHOICES = {
    ('1', 'public'),
    ('2', 'private'),
}

class Request(models.Model):
    user = models.CharField(max_length=22, default='current user')
    requested = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):
    user = models.CharField(max_length=22, default='current user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.SmallIntegerField(choices=FRIEND_CATEGORY_CHOICES, default=1)
    status = models.SmallIntegerField(choices=FRIEND_STATUS_CHOICES, default=1)
    created = models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    name = models.CharField(max_length = 25)
    description = models.CharField(max_length = 250, null=True)
    count = models.SmallIntegerField(default=1)
    status = models.SmallIntegerField(choices=GROUP_STATUS_CHOICES, default=1)
    reference_code = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) #user
    group = models.ForeignKey(Group, default=1 , on_delete=models.CASCADE) #user
    status = models.SmallIntegerField(choices=MEMBER_STATUS_CHOICES, default=1) #user
    funding = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    created = models.DateTimeField(auto_now_add=True) #server

class Record(models.Model):
    description = models.CharField(max_length=20, default='group expense')
    split = models.SmallIntegerField(default=1) #user
    count = models.IntegerField(default=0)
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

class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    memo = models.CharField(max_length=200, default='money transfer')
    transfer = models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

class GroupBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    memo = models.CharField(max_length=200, default='group transfer')
    transfer = models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #server
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True) #server
    description = models.CharField(max_length=200) #server
    status = models.SmallIntegerField(default=1)
    category = models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True) #server

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    description = models.CharField(max_length=200)  # server
    status = models.SmallIntegerField(default=1)  # server
    category = models.SmallIntegerField(default=1)  # server
    created = models.DateTimeField(auto_now_add=True)  # server

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    first_name = models.CharField(max_length=25, default='first')
    last_name = models.CharField(max_length=25, default='last')
    dob = models.DateField(default='1950-01-01')
    street = models.CharField(max_length=200, default='street address')
    city = models.CharField(max_length=100, default='city')
    state = USStateField(default='CA')
    zip_code = models.IntegerField(default=12345)
    phone = models.BigIntegerField(default=0)  # user
    # synapse_id = models.CharField(max_length=220, default=000000)
    privacy = models.SmallIntegerField(default=1)  # user
    balance = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    dwolla_id = models.CharField(max_length=200, default='https://api-sandbox.dwolla.com')
    created = models.DateTimeField(auto_now_add=True)  # server

# the following need to be sent with the paypal api to create a new user within
# the applicaiton. account-type, address, citizenship-code, governament-id, account-web-option,
# currency-code, dob, email, name, language-code, reg-type, request-envelope

class Transfers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main = models.CharField(max_length=150, default='account')
    transfer = models.CharField(max_length=150, default='accont')
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    memo = models.CharField(max_length=200, default='memo')
    frequency = models.SmallIntegerField(default=1)
    status = models.SmallIntegerField(default=1)
    create = models.DateTimeField(auto_now_add=True)

class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.CharField(max_length=50, default='Wells Fargo')
    name = models.CharField(max_length=50, default='Account')
    created = models.DateTimeField(auto_now_add=True)

#----- The following is a potential model class for the new profile settings ---
# the following are a list of all the different objects that are needed for the
# paypal api. []
