from django.conf.urls import url
from . import views

# FOR ALL OF THE LINKS THAT HAVE A PASSED IN INTEGER VARIABLE VALUE, GO TO THE
# ACCOUNTS URL AND YOU WILL BE ABLE TO SEE EVERY RECORD IN THE DATABASE FOR all
# OF THE STUFF I DID (GROUPS, MEMBERS, RECORDS, TRANSACTIONS, USERS). YOU WILL
# USE THEN WHEN PASSING IN LINKS.
urlpatterns = [
    url(r'^$', views.userHome, name='home_page'),
    url(r'^login$', views.login_page, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.logout_page, name='logout'),
    url(r'^setup_profile/$', views.profile_setup, name='profile_setup'),
    url(r'^user_balance/$', views.userTransfer, name='user_balance'),
    url(r'^(?P<requested>[\w+]+)/sendRequest/$', views.sendRequest, name="send_request"),
    url(r'^(?P<accepted>[\w+]+)/acceptRequest/$', views.acceptRequest, name="accept_request"),
    url(r'^createGroup/$', views.createGroup, name='create_group'),
    # for this url, you will have to enter the group id and then add members to
    # the url. an example would be 127.0.0.1:8000/3/addMembers
    url(r'^(?P<groupId>[0-9]+)/add_members/$', views.addMembers,
        name='add_members'),
    # this url is going to be the same as the one above but with the addRecord
    # at the end to add a new record or expense to the group
    url(r'^(?P<groupId>[0-9]+)/add_record/$', views.addRecord,
    name='add_record'),
    # when you want to add a transaction which is the part that will be where the
    # user splits the bill evenly or individually and enters the amount for the
    # expense and checks to make sure everything is correct before creating the expense
    url(r'^(?P<groupId>[0-9]+)/(?P<recordId>[0-9]+)/add_transaction/$',
        views.addTransaction, name='add_transactions'),
    url(r'^group/(?P<groupId>[0-9]+)/$', views.groupHome, name='group_home'),
    url(r'^(?P<groupId>[0-9]+)/group_balance/$', views.groupTransfer, name='group_balance'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/delete$', views.accountsDelete, name='delete_accounts'),
    # # the following is to just test the sypanse api
    # url(r'^create_user_synapse$', views.createUserSynapse, name='create_user_synapse')
]
