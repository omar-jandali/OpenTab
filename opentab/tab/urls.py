from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^createGroup/$', views.groups, name='create_group'),
    url(r'^addMembers/$', views.addMembers, name='add_four_members'),
    url(r'^accounts/$', views.accounts, name='accounts'),
]
