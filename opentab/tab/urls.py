from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^createGroup/$', views.groups, name='create_group'),
    url(r'^(?P<groupName>[\w+]+)/addMembers/$', views.addMembers,
        name='add_members'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^(?P<name>[\w+]+)/home/$', views.userHome, name='user_home')
]
