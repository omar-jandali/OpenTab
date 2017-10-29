from django.conf.urls import url
from . import views

# FOR ALL OF THE LINKS THAT HAVE A PASSED IN INTEGER VARIABLE VALUE, GO TO THE
# ACCOUNTS URL AND YOU WILL BE ABLE TO SEE EVERY RECORD IN THE DATABASE FOR all
# OF THE STUFF I DID (GROUPS, MEMBERS, RECORDS, TRANSACTIONS, USERS). YOU WILL
# USE THEN WHEN PASSING IN LINKS.
urlpatterns = [
    url(r'^$', views.userGroups, name='home_page'),
    url(r'^login$', views.loginPage, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.logoutPage, name='logout'),
    url(r'^setup_profile/$', views.profileSetup, name='profile_setup'),
    url(r'^settings/$', views.userSettings, name='user_settings'),
    url(r'^groups/$', views.userGroups, name='user_groups'),
    url(r'^profile/$', views.userHome, name='user_home'),
    url(r'^searched/$', views.searchedUser, name='user_search'),
    url(r'^accounts/$', views.userAccounts, name='user_accounts'),
    url(r'^expenses/$', views.userExpenses, name='user_expenses'),
    url(r'^clear_all_activities/$', views.clearAllActivities, name='clear_all_activities'),
    url(r'^transfer/$', views.transfers, name='transfer'),
    url(r'^template_testing/$', views.templateTesting, name='template_testing'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^link_account/$', views.linkAccount, name='link_account'),
    url(r'^linked_accounts/$', views.linkedAccounts, name='linked_accounts'),
    url(r'^default_source/(?P<source_id>[0-9]+)/$', views.setDefaultSource, name='default_source'),
    url(r'^login_synapse/$', views.loginAccountSynapse, name='login_synapse'),
    url(r'^linked_synapse/$', views.listedLinkAccounts, name='linked_synapse'),
    url(r'^sample_transaction/$', views.createTransaction, name='sample_transaction'),
    url(r'^createGroup/$', views.createGroup, name='create_group'),
    url(r'^template_test/$', views.templateTesting, name='template_testing'),
    url(r'^single_expense/$', views.addExpenseSingle, name='single_expense'),
    url(r'^(?P<requested>[\w+]+)/sendRequest/$', views.sendRequest, name="send_request"),
    url(r'^(?P<accepted>[\w+]+)/acceptRequest/$', views.acceptRequest, name="accept_request"),
    # for this url, you will have to enter the group id and then add members to
    # the url. an example would be 127.0.0.1:8000/3/addMembers
    url(r'^(?P<groupId>[0-9]+)/add_members/$', views.addMembers, name='add_members'),
    url(r'^(?P<groupId>[0-9]+)/(?P<memberName>[\w+]+)/select_host_member/$', views.selectHostMember,
        name='select_host_member'),
    url(r'^(?P<groupId>[0-9]+)/add_expense/$', views.addExpense, name="add_expense"),
    url(r'^(?P<groupId>[0-9]+)/(?P<groupName>[\w+]+)/update_expense_even/$',
        views.updateExpenseEven, name="update_expense_even"),
    url(r'^(?P<groupId>[0-9]+)/(?P<groupName>[\w+]+)/update_expense_individual/$',
        views.updateExpenseIndividual, name="update_expense_individual"),
    url(r'^(?P<reference>[0-9]+)/update_expense_even_single/$',
        views.updateExpenseEvenSingle, name="update_expense_even_single"),
    url(r'^(?P<reference>[0-9]+)/update_expense_individual_single/$',
        views.updateExpenseIndividualSingle, name="update_expense_individual_single"),
    url(r'^group/(?P<groupId>[0-9]+)/$', views.groupHome, name='group_home'),
    url(r'^(?P<expenseId>[0-9]+)/(?P<activityId>[0-9]+)/verify_expense/$', views.verifyExpense, name='verify_expense'),
    url(r'^(?P<userName>[\w+]+)/$', views.userProfile, name='user_profile'),
    # the following is to just test the sypanse api
    # url(r'^create_user_synapse$', views.createUserSynapse, name='create_user_synapse')
]
