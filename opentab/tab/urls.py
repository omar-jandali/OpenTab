from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^createGroup/$', views.groups, name='create_group'),
    url(r'^(?P<groupName>[\w+]+)/addMembers/$', views.addMembers,
        name='add_members'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/delete$', views.accountsDelete, name='delete_accounts'),
    url(r'^(?P<name>[\w+]+)/user/home/$', views.userHome, name='user_home'),
    url(r'^(?P<groupName>[\w+]+)/group/home/$', views.groupHome, name='group_home'),
    url(r'^(?P<groupName>[\w+]+)/group/addRecord/$', views.addRecord,
        name='add_record'),
]
