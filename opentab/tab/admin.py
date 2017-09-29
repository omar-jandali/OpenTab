from django.contrib import admin
from .models import Group, Member, Request, Friend, Activity
from .models import Notification, Profile

admin.site.register(Friend)
admin.site.register(Group)
admin.site.register(Member)
