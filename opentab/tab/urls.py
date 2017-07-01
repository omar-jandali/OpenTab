from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login_page, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^loggedin$', views.logged_in, name='logged_in'),
    url(r'^logout$', views.logout_page, name='logout_page'),
    url(r'^createGroup/$', views.groups, name='create_group'),
    url(r'^(?P<groupId>[0-9]+)/addMembers/$', views.addMembers,
        name='add_members'),
    url(r'^(?P<groupId>[0-9]+)/addRecord/$', views.addRecord,
    name='add_record'),
    url(r'^(?P<groupId>[0-9]+)/(?P<recordId>[0-9]+)/addTransaction/$',
        views.addTransaction, name='add_transactions'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/delete$', views.accountsDelete, name='delete_accounts'),
    url(r'^(?P<name>[\w+]+)/homes/$', views.userHome, name='user_home'),
    url(r'^(?P<groupId>[0-9]+)/home/$', views.groupHome, name='group_home'),
]
