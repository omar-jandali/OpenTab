from django.conf.urls import url
from . import views

# FOR ALL OF THE LINKS THAT HAVE A PASSED IN INTEGER VARIABLE VALUE, GO TO THE
# ACCOUNTS URL AND YOU WILL BE ABLE TO SEE EVERY RECORD IN THE DATABASE FOR all
# OF THE STUFF I DID (GROUPS, MEMBERS, RECORDS, TRANSACTIONS, USERS). YOU WILL
# USE THEN WHEN PASSING IN LINKS.
urlpatterns = [
    url(r'^login$', views.login_page, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.logout_page, name='logout_page'),
    url(r'^$', views.userHome, name='homePage'),
    url(r'^(?P<requested>[\w+]+)/sendRequest/$', views.sendRequest, name="sendRequest"),
    url(r'^(?P<accepted>[\w+]+)/acceptRequest/$', views.acceptRequest, name="acceptRequest"),
    url(r'^(?P<groupId>[0-9]+)/home/$', views.groupHome, name='group_home'),
    url(r'^createGroup/$', views.createGroup, name='create_group'),
    # for this url, you will have to enter the group id and then add members to
    # the url. an example would be 127.0.0.1:8000/3/addMembers
    url(r'^(?P<groupId>[0-9]+)/addMembers/$', views.addMembers,
        name='add_members'),
    # this url is going to be the same as the one above but with the addRecord
    # at the end to add a new record or expense to the group
    url(r'^(?P<groupId>[0-9]+)/addRecord/$', views.addRecord,
    name='add_record'),
    # when you want to add a transaction which is the part that will be where the
    # user splits the bill evenly or individually and enters the amount for the
    # expense and checks to make sure everything is correct before creating the expense
    url(r'^(?P<groupId>[0-9]+)/(?P<recordId>[0-9]+)/addTransaction/$',
        views.addTransaction, name='add_transactions'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/delete$', views.accountsDelete, name='delete_accounts'),
]
