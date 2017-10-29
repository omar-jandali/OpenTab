from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# the following is what gives the states to select from when it comes to the states
# field in the model
from django_localflavor_us.models import USStateField

class Request(models.Model):
    user = models.CharField(max_length=22, default='current user')
    requested = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):
    user = models.CharField(max_length=22, default='current user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.SmallIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    name = models.CharField(max_length = 25)
    description = models.CharField(max_length = 250, null=True)
    count = models.SmallIntegerField(default=1)
    status = models.SmallIntegerField(default=1)
    reference_code = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) #user
    group = models.ForeignKey(Group, default=1 , on_delete=models.CASCADE) #user
    status = models.SmallIntegerField(default=1) #user
    funding = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    created = models.DateTimeField(auto_now_add=True) #server

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    description = models.CharField(max_length=200, default = 'expense')
    name = models.CharField(max_length=100, default = 'group name')
    location = models.CharField(max_length=100, default = 'location')
    status = models.SmallIntegerField(default = 1)
    split = models.SmallIntegerField(default = 1)
    reference = models.IntegerField(default = '101', null = True)
    created_by = models.CharField(max_length = 200, default = 'username', null=True)
    created = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    first_name = models.CharField(max_length=25, default='first')
    last_name = models.CharField(max_length=25, default='last')
    bio = models.CharField(max_length=220, default='bio')
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
    synapse_id = models.CharField(max_length=200, default='123456789')
    created = models.DateTimeField(auto_now_add=True)  # server

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(max_length=150, null=True)
    expense = models.ForeignKey(Expense, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='some action')
    accepted = models.SmallIntegerField(default = 1)
    # 1 = unseen 2 = seen
    status = models.SmallIntegerField(default=1)
    reference = models.IntegerField(default = '101', null = True)
    validation = models.SmallIntegerField(default = 1)
    created = models.DateTimeField(auto_now_add=True)

class GroupActivity(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    host = models.CharField(max_length=100, null=True)
    expense = models.ForeignKey(Expense, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='some action')
    # the following will allow the group to know if it is a general group activity
    # or if there is a user specificied
    general = models.SmallIntegerField(default = 1)
    validation = models.SmallIntegerField(default = 1)
    accepted = models.SmallIntegerField(default = 1)
    created = models.DateTimeField(auto_now_add=True)


# the following values:
# 1 - everyone
# 2 - friends
# 3 - only me

class Privacy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groups = models.SmallIntegerField(default=1)
    friends = models.SmallIntegerField(default=1)
    expenses = models.SmallIntegerField(default=1)
    searchable = models.SmallIntegerField(default=1)

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

# The following model is going to be used to create a record and store all the informaitno
# related to each users dwolla account for easy access within the dwolla api and the app
# methods that are going to work with the Dwolla api directly

class Dwolla(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=100, default='customer id')
    source_id = models.CharField(max_length=100, default='funding source')
    status = models.SmallIntegerField(default=1)


# The following models are going to be used to store all of the synapse api informaiton
# related to the currentUser. THis includes id, accounts, transfers, and more

# the following is going to store important credentials for synapse users
class SynapseUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    _id = models.IntegerField()
    cip_tag = models.IntegerField()
    link = models.CharField(max_length=200, default='https://uat-api.synapsefi.com/v3.1')

class SynapseAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    _id = models.CharField(max_length=200, default = '1234567890')
    cip_tag = models.IntegerField()
