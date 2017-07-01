from django.contrib import admin
from .models import Friend, Group, Member, Request, Activity, Record, Transaction
from .models import Notification, Profile

admin.site.register(Friend)
admin.site.register(Group)
admin.site.register(Member)
