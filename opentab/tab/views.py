from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import formset_factory
from django.db.models import Q
import os, requests, json

from random import randint
from decimal import Decimal
from pprint import pprint

from .models import Group, User, Member, Request, Friend, Profile, Expense, Privacy
from .models import Accounts, Transfers, Dwolla, UserActivity, GroupActivity

from .forms import CreateGroupForm, AddMembersForm, UserSettingsTwoForm, UserSettingsForm
from .forms import SignupForm, LoginForm, ProfileForm, UpdatePasswordForm, UpdateInfoForm
from .forms import TransferForm, LinkAccountForm, LinkAccountSynapse, ExpenseForm
from .forms import UpdateExpenseEvenForm, UpdateExpenseIndividualForm, UpdatePrivacyForm

import dwollav2
from synapse_pay_rest import Client, Node, Transaction
from synapse_pay_rest import User as SynapseUser
from synapse_pay_rest.models.nodes import AchUsNode

#-------------------------------------------------------------------------------
# the following code is going to be for the Dwolla API configuration
#-------------------------------------------------------------------------------

#the following is going to be the access token, key, secet for the dwolla sandbox
token = 'ZIguu9oOb4aeq2qS0YUGt1T8WOnt73GSki3EHIyJ1jPE1EspdX'
app_key = 'o8TsxKanLqGxoTKDas9dY8RCXpQ3hEeWussEEmhyLbdmED3s62'
app_secret = 'haUMr5aKf9zpMQDUMugcaLFOUg47oHYBRew64p65O2nGkLa11F'

# initiates the connection between the api and opentab
client = dwollav2.Client(
    key = app_key,
    secret = app_secret,
    environment = "sandbox"
)

#-------------------------------------------------------------------------------
# the following is going to be where the synspase api is going to be initiated and
# connection between the api and this app is going to be made and verified.
#-------------------------------------------------------------------------------

# the following are all of the different credentials that are needed in order to
# initiate the connect between the api and opentab
APP_CLIENT_ID = 'client_id_SOJMCFkagKAtvTpem0ZWPRbwznQ2yc5h0dN6YiBl'
APP_CLIENT_SECRET = 'client_secret_muUbizcGBq2oXKQTMEphg0S4tOyH5xLYNsPkC3IF'
APP_FINGERPRINT = '599378e9a63ec2002d7dd48b'
APP_IP_ADRESS = '127.0.0.1'

# the following are going to be all of the different credentials that are going
# to be needed in order to establish connection
args = {
    'client_id':APP_CLIENT_ID,
    'client_secret':APP_CLIENT_SECRET,
    'fingerprint':APP_FINGERPRINT,
    'ip_address':APP_IP_ADRESS,
    'development_mode':True,
    'logging':False,
}

# this is the call that takes the credentials and sends the connect request to
# validate credentials
client = Client(**args)
print(client)

#-------------------------------------------------------------------------------
# the following section is the actual code for the core of the project. Not an
# api function. this is the self written code that will reate and run the application
#-------------------------------------------------------------------------------

# The signup method is where all of the processing and display of the users signup
# screen. The form asks for username, password, verify the password, and the email
def signup(request):
    # the following will determine if the form is submitted or not
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # the following section validates the entire form and processed the data
        if form.is_valid():
            # the following will make sure the data is clean and then store them
            # into new variables
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            verify = cd['verify']
            email = cd['email']
            # the folloiwng will make sure the password and verification are matching
            # before storing the info into the database
            if password == verify:
                # the following will hash the password
                secure_password = make_password(password)
                new_user = User.objects.create(
                    username = username,
                    password = secure_password,
                    email = email,
                )
                # the following will store the username of the account that was just
                # created in to the session so that the app can track the user that
                # is logged in
                request.session['username'] = username
                return redirect('profile_setup')
            else:
                # if password and verification dont match, a message will be sent
                # back to the user so they can fill in the correct info.
                message = 'Password and Verify dont match'
                parameters = {
                    'form':form,
                    'message':message,
                }
                return render(request, 'tabs/signup.html', parameters)
    else:
        # this will display the form if it waas not submmited.
        form = SignupForm()
        message = 'Fill out the form'
        parameters = {
            'form':form,
            'message':message,
        }
        return render(request, 'tabs/signup.html', parameters)

# The following is the method that will display and process the users login page
def loginPage(request):
    # the following will check to see if the form is submitted or not.
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # the following validates the form and will store the cleaned data that the
        # user submitted.
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            # the following line will authenticate the user based on the username
            # and password that was submiited.
            user = authenticate(username=username, password=password)
            # if the user ;is authentic, the username will be stored in the session
            # and redirect the user to their home page.
            if user:
                request.session['username'] = username
                profiles = Profile.objects.all()
                for profile in profiles:
                    if profile.user.username == user.username:
                        return redirect('user_groups')
            else:
                # if the user is not authentic, a error message will be displayed
                # and the user will have to re login
                message = 'invalid login info'
                parameters = {
                    'message':message,
                    'form':form,
                }
            return render(request, 'tabs/login.html', parameters)
    else:
        # this will display the login form if it was not submitted initially
        form = LoginForm()
        message = 'Login Below'
        parameters = {
            'form':form,
            'message':message,
        }
        return render(request, 'tabs/login.html', parameters)


# this is a page that the user is redirected to once they register or choose to update
# through the main page. This is where the user will create their profile by providing
# specified informaiton.
def profileSetup(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        # the following is just going to grab the currently logged in user and
        # save the profile information to the appropriate user
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        # the following is the provessing for the form where the user entered
        # the profile informaiton
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                first_name = cd['first_name']
                last_name = cd['last_name']
                dob = cd['dob']
                city = cd['city']
                state = cd['state']
                phone = cd['phone']
                privacy = cd['privacy']
                # this is the new record that is going to be created and saved
                new_profile = Profile.objects.create(
                    user = currentUser,
                    first_name = first_name,
                    last_name = last_name,
                    dob = dob,
                    city = city,
                    state = state,
                    phone = phone,
                    privacy = privacy,
                )

                # the follownig is gong to be the activity for setting up a profile_setup
                description = 'Welcome ' + currentUser.username + ', you have created your new Yap profile'
                profile_activity = UserActivity.objects.create(
                    user = currentUser,
                    description = description,
                    status = 1
                )
                createUserSynapse(request)
                return redirect('user_groups')
        else:
            # this is what is going to be saved into the html file and used to
            # render the file
            form = ProfileForm()
            message = 'fill out form below'
            parameters = {
                'form':form,
                'currentUser':currentUser,
                'message':message,
            }
            return render(request, 'tabs/profile_setup.html', parameters)

# The following view is what will be used to display all of the groups and informaiton
# for the logged in user including groups balances and friends
# Passed in var:
#   name = the name of the user that is logged in
def userHome(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    activities = UserActivity.objects.filter(user = currentUser).all()
    unseen_activity = UserActivity.objects.filter(user = currentUser).filter(status=1).filter(account=None).count()

    requester = Request.objects.filter(user = currentUser.username).all()
    requested = Request.objects.filter(requested = currentUser).all()

    requests = requester | requested

    friender = Friend.objects.filter(user = currentUser.username).all()
    friended = Friend.objects.filter(friend = currentUser).all()

    friends = friender | friended

    parameters = {
        'currentUser':currentUser,
        'activities':activities,
        'unseen_activity':unseen_activity,
        'requests':requests,
        'friends':friends
    }

    return render(request, 'tabs/user_home.html', parameters)

def userExpenses(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    activities = UserActivity.objects.filter(user = currentUser).all()

    parameters = {
        'currentUser':currentUser,
        'activities':activities,
    }

    return render(request, 'tabs/user_expenses.html', parameters)

def userGroups(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    members = Member.objects.filter(user = currentUser).all()

    if request.method == "POST":
        cheese = 'hello'
    else:
        parameters = {
            'currentUser':currentUser,
            'members':members,
        }
        return render(request, 'tabs/user_groups.html', parameters)

def userAccounts(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    parameters = {
        'currentUser':currentUser
    }
    return render(request, 'tabs/user_accounts.html', parameters)

def userSettings(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # commented during initial testing because of dumplcate objects
    #currentPrivacy = Privacy.objects.get(user = currentUser)
    currentPrivacy = Privacy.objects.filter(user = currentUser).first()
    passwordMessage = ''
    if request.method == "POST":
        if 'userSubmit' in request.POST:
            updateUserOne = UserSettingsForm(request.POST)
            if updateUserOne.is_valid():
                cd = updateUserOne.cleaned_data
                username = cd['username']
                email = cd['email']
            updateUserTwo = UserSettingsTwoForm(request.POST)
            if updateUserTwo.is_valid():
                cd = updateUserTwo.cleaned_data
                first_name = cd['first_name']
                last_name = cd['last_name']
                bio = cd['bio']
                # the following is going to update the appropriate records in the
                # table with the updated correct informaiton
                update_user = currentUser
                update_user.username = username
                update_user.email = email
                update_user.save()
                update_profile = currentProfile
                update_profile.first_name = first_name
                update_profile.last_name = last_name
                update_profile.bio = bio
                update_profile.save()
                updateSessionUsername(request, update_user.username)

                # new activity for updating your profile
                description = 'You have updated your user profile'
                user_profile_update = UserActivity.objects.create(
                    user = currentUser,
                    description = description,
                    status = 1
                )

                return redirect('home_page')
        if 'passwordSubmit' in request.POST:
            updatePassword = UpdatePasswordForm(request.POST)
            if updatePassword.is_valid():
                cd = updatePassword.cleaned_data
                current_password = cd['current_password']
                new_password = cd['new_password']
                verify_password = cd['verify_password']
                user = authenticate(username=currentUser.username, password=current_password)
                if user:
                    if new_password == verify_password:
                        secured_password = make_password(new_password)
                        update_user = currentUser
                        update_user.password = secured_password
                        update_user.save()

                        # new activity for updating your profile
                        description = 'You have updated your password'
                        user_profile_update = UserActivity.objects.create(
                            user = currentUser,
                            description = description,
                            status = 1
                        )

                        return redirect('home_page')
                    else:
                        passwordMessage = 'The two passwords do not match'
                        # if the passwords do no match
                else:
                    passwordMessage = 'Current password does not match our records'
                    # in case the old password is not what is saved in the database
        if 'infoSubmit' in request.POST:
            updateInfo = UpdateInfoFOrm(request.POST)
            if updateInfo.is_valid():
                cd = updateInfo.cleaned_data
                phone = cd['phone']
                dob = cd['dob']
                street = cd['street']
                city = cd['city']
                state = cd['state']
                zip_code = cd['zip_code']
                update_profile = currentProfile
                update_profile.phone = phone
                update_profile.dob = dob
                update_profile.street = street
                update_profile.city = city
                update_profile.state = state
                update_profile.zip_code = zip_code
                update_profile.save()

                # new activity for updating your profile
                description = 'You have updated your profile info'
                user_profile_update = UserActivity.objects.create(
                    user = currentUser,
                    description = description,
                    status = 1
                )

                return redirect('home_page')
        if 'privacySubmit' in request.POST:
            updatePrivacy = UpdatePrivacyForm(request.POST)
            if updatePrivacy.is_valid():
                cd = updatePrivacy.cleaned_data
                groups = cd['groups']
                friends = cd['friends']
                expenses = cd['expenses']
                searchable = cd['searchable']
                update_privacy = currentPrivacy
                update_privacy.groups = groups
                update_privacy.friends = friends
                update_privacy.expenses = expenses
                update_privacy.searchable = searchable
                update_privacy.save()

                # new activity for updating your profile
                description = 'You have updated your privacy settings'
                user_profile_update = UserActivity.objects.create(
                    user = currentUser,
                    description = description,
                    status = 1
                )

                return redirect('home_page')
    userSettingOne = UserSettingsForm(instance=currentUser)
    userSettingTwo = UserSettingsTwoForm(instance=currentProfile)
    updatePassword = UpdatePasswordForm()
    updateInfo = UpdateInfoForm(instance=currentProfile)
    updatePrivacy = UpdatePrivacyForm()

    parameters = {
        'currentUser':currentUser,
        'currentProfile':currentProfile,
        'currentPrivacy':currentPrivacy,
        'userSettingOne':userSettingOne,
        'userSettingTwo':userSettingTwo,
        'updatePassword':updatePassword,
        'updateInfo':updateInfo,
        'updatePrivacy':updatePrivacy,
        'passwordMessage':passwordMessage,
    }
    return render(request, 'tabs/user_settings.html', parameters)

def searchedUser(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    users = User.objects.all()

    if request.method == 'POST':
        searched = request.POST['searched']

        for user in users:
            if user.username == searched:
                searchedUser = user
                return redirect('user_profile', userName = searchedUser.username)
        return redirect('user_groups')


def userProfile(request, userName):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    viewedUser = None
    viewedProfile = None

    users = User.objects.all()
    for user in users:
        if user.username == userName:
            viewedUser = user
            viewedProfile = Profile.objects.get(user = viewedUser)

    if viewedUser != None:
        friends = Friend.objects.filter(Q(user = currentUser.username, friend = viewedUser) | Q(user = viewedUser.username, friend = currentUser))

    if friends:
        print('friends')
    else:
        friends = None
        print('not friends')

    parameters = {
        'currentUser':currentUser,
        'currentProfile':currentProfile,
        'viewedUser':viewedUser,
        'viewedProfile':viewedProfile,
        'friends':friends
    }
    return render(request, 'tabs/user_profile.html', parameters)

# the following method managed the sending of friend requests to other users and
# storing a record of that in the database.
def sendRequest(request, requested):
    currentUser = loggedInUser(request)
    # the following will grab the user object with the username that was submitted
    # for the friend request.
    requestedUser = User.objects.get(username = requested)
    # the following created a new record in the request table within the database.
    if requestedUser:
        new_request = Request.objects.create(
            user = currentUser,
            requested = requestedUser,
        )

        description = currentUser.username + ' has send you a friend request'
        request_activity = UserActivity.objects.create(
            user = requestedUser,
            description = description,
            status = 1,
        )
    return redirect('home_page')

# The following method will process the acceptaance of a friend request.
def acceptRequest(request, accepted):
    currentUser = loggedInUser(request)
    acceptedUser = User.objects.get(username = accepted)
    # a new record will be added to the Friend table in teh database that will
    # be later used as a way to display all of a users friends.
    new_friend = Friend.objects.create(
        user = currentUser,
        friend = acceptedUser,
        category = 1
    )

    accepted_description = 'You and ' + acceptedUser.username + ' are now friends'
    friend_description = 'You and ' + currentUser.username + ' are now friends'
    accepted_activity = UserActivity.objects.create(
        user = currentUser,
        description = accepted_description,
        status = 1
    )

    friend_activity = UserActivity.objects.create(
        user = acceptedUser,
        description = friend_description,
        status = 1
    )

    # after the new friend record is created, the original request is found
    # and deleted so that they request does not keep showing up on the logged in
    # users home page.
    requests = Request.objects.filter(requested = currentUser).all()
    for request in requests:
        if request.user == acceptedUser.username:
            request.delete()
    return redirect('home_page')

# The view is g0ing to be used to create the group and add the information for the
# group before creating the record in the database. It will also be incharge of adding
# the first memeber to the group (the person who created the group).

#  will redirect to the adding memeber view (need to be fixed)
def createGroup(request):
    currentUser = loggedInUser(request)
    # following is all of th actions that are taken after the form is submitted
    if request.method == 'POST':
        # the following few lines will get the submitted form and create a reference
        # code that is going to be used later.
        # it will also assign the user that created the group
        form = CreateGroupForm(request.POST)
        referenceCode = generateReferenceNumber()
        # the following validated the actual form to ensure that it was filled out
        # with the correct inforamtion
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            description = cd['description']
            # the new_group creates an isntance of the new group and saved it into
            # the database once it is created.
            new_group = Group.objects.create(
                name = name,
                description = description,
                reference_code = referenceCode,
                created_by = currentUser,
            )

            user_description = 'You created a new group - ' + name

            user_activity = UserActivity.objects.create(
                user = currentUser,
                description = user_description,
                status = 1,
            )


            # return redirect('home_page')
            return redirect('add_members', groupId=new_group.id)
            #return redirect('accounts')
            #return redirect(reverse('add_members', args=[new_group.id]))
    else:
        # the following is the storing of the forms
        form = CreateGroupForm()
        message = 'enter group info below'
    # the following are all the objects that are going to be passed to the
    # rendering remplate
        parameters = {
            'form':form,
            'message':message,
        }
    return render(request, 'tabs/create_group.html', parameters)

# The following is the view that will manage the groups profile. It will be the main
# page that users will be able to use to find all of the different information
# regarding the specific group that is selected.
# Passed in var:
# groupId = the id of the group that is selected (will be changed to the group name
# later into the development)
def groupHome(request, groupId):
    currentUser = loggedInUser(request)
    group = Member.objects.filter(user = currentUser).filter(group = groupId).first()
    # the following is going to be the currentGroup by groupId
    currentGroup = Group.objects.get(id = groupId)
    # the following is the group object with the id that is passed in the url
    # group = Group.objects.get(name = groupName)
    members = Member.objects.filter(group = group.group).all()
    for member in members:
        if member.status == 2:
            host = member

    activities = GroupActivity.objects.filter(group = currentGroup).all()

    expenses = Expense.objects.filter(group = group.group).all()

    parameters = {
        'members':members,
        'group':group,
        'currentGroup':currentGroup,
        'currentUser':currentUser,
        'expenses':expenses,
        'host':host,
        'activities':activities,
    }
    return render(request, 'tabs/group_home.html', parameters)

# This view is what will add different members to the gorup that is selected. This
# method will be in charge of not only adding the member to the group and keeping
# a record of it in the database, but also keep track of the number of members in
# the group so that it is easily calculated later.
# Passed in var:
#   groupId - the id of the group that the memeber will be added to.
def addMembers(request, groupId):
    currentUser = loggedInUser(request)
    # the following line will grab the group object that members will be added ot and
    # stored in a variable that will be referenced later.
    groups = Group.objects.filter(id = groupId).all()
    # the following will grab all of the member objects that are related to the logged
    # in user.
    group = Group.objects.get(id = groupId)
    users = User.objects.all()
    friends = Friend.objects.all()
    # the form is similar to the form submition above for reference
    if request.method == "POST":
        # the following sets the current user as a member of the group once the
        # group is created as a default
        new_default_member = Member.objects.create(
            user = currentUser,
            group = group,
            status = 2,
        )

        default_description = currentUser.username + ' created ' + group.name
        default_activity = GroupActivity.objects.create(
            group = group,
            description = default_description,
        )
        # the following will scroll through every user in the users table
        for friend in friends:
            # it will then check to see if the usersname was returned in the request.
            # if the username was checked, it will be returned, otherwise it will not
            # be passed.
            if friend.user == currentUser.username:
                selected_user = User.objects.get(username = friend.friend.username)
                if selected_user.username in request.POST:
                    new_member = Member.objects.create(
                        user = selected_user,
                        group = group,
                        status = 1,
                    )

                    friend_description = currentUser.username + ' added you to ' + group.name
                    group_description = currentUser.username + ' added ' + selected_user.username + ' to ' + group.name

                    group_member_activity = GroupActivity.objects.create(
                        user = selected_user,
                        group = group,
                        description = group_description,
                        general = 1
                    )

                    friend_member_activity = GroupActivity.objects.create(
                        user = selected_user,
                        group = group,
                        description = friend_description,
                        general = 2,
                    )

            if friend.friend.username == currentUser.username:
                selected_user = User.objects.get(username = friend.user)
                print(selected_user)
                if selected_user.username in request.POST:
                    new_member = Member.objects.create(
                        user = selected_user,
                        group = group,
                        status = 1,
                    )

                    friend_description = currentUser.username + ' added you to ' + group.name
                    group_description = currentUser.username + ' added ' + selected_user.username + ' to ' + group.name

                    group_member_activity = GroupActivity.objects.create(
                        user = selected_user,
                        group = group,
                        description = group_description,
                        general = 1
                    )

                    friend_member_activity = GroupActivity.objects.create(
                        user = selected_user,
                        group = group,
                        description = friend_description,
                        general = 2
                    )

                # next three lines will keep track and updated the group count every time that
                # a new user is added to the specific group that is selected.
                updated_group = group
                updated_group.count = updated_group.count + 1
                updated_group.save()
        return redirect('group_home', groupId=group.id)
    else:
        # the form that the user fills out will display all of the members of the
        # app and the current user will select the checkbox next to the name
        # of the user that he wants to add to the group. THIS WILL CHANGE TO DISPLAY
        # FRIENDS AFTER THE FRIENDS MODEL AND FUNCTION ARE CREATED
        message = 'add members below'
        params = {
            'message':message,
            'group':group,
            'users':users,
            'friends':friends,
            'currentUser':currentUser,
        }
    return render(request, 'tabs/add_members.html', params)

def selectHostMember(request, groupId, memberName):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    currentGroup = Group.objects.get(id = groupId)
    members = Member.objects.filter(group = currentGroup)
    for member in members:
        if member.status == 2:
            host = member
            print(host.user.username)
        if member.user.username == memberName:
            selectedMember = member
            print(selectedMember.user.username)

    old_host = host
    old_host.status = 1
    old_host.save()

    new_host = selectedMember
    new_host.status = 2
    new_host.save()

    group_description = selectedMember.user.username + ' is the new group host'
    group_activity = GroupActivity.objects.create(
        group = currentGroup,
        description = group_description,
    )

    return redirect('group_home', groupId = currentGroup.id)

def addExpense(request, groupId):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    currentGroup = Group.objects.get(id = groupId)
    members = Member.objects.filter(group = currentGroup).all()

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            location = cd['location']
            split = cd['split']
            for member in members:
                if member.user.username in request.POST:
                    new_expense = Expense.objects.create(
                        user = member.user,
                        group = currentGroup,
                        name = name,
                        location = location,
                        split = split,
                    )
            description = 'New expense: ' + new_expense.name + ' - ' + new_expense.location
            expense_activity = GroupActivity.objects.create(
                group = currentGroup,
                expense = new_expense,
                description = description
            )

        if split == 1:
            return redirect('update_expense_even', groupId = currentGroup.id, groupName = name)
        if split == 2:
            return redirect('update_expense_individual', groupId = currentGroup.id, groupName = name)
    else:
        form = ExpenseForm()
        message = 'Please fill out the form'
        parameters = {
            'form':form,
            'message':message,
            'members':members,
            'currentGroup':currentGroup,
        }
        return render(request, 'tabs/add_expense.html', parameters)

def updateExpenseEven(request, groupId, groupName):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    currentGroup = Group.objects.get(id = groupId)
    host = Member.objects.filter(group = groupId).filter(status = 2).first()
    expenses = Expense.objects.filter(group = currentGroup).filter(name = groupName).all()
    expenses_count = Expense.objects.filter(group = currentGroup).filter(name = groupName).count()
    if request.method == "POST":
        form = UpdateExpenseEvenForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            amount = cd['amount']
            userAmount = SplitEven(expenses_count, amount)
            # the followig is going to update the expenses that were created with the
            # split amounts and description for the expense
            for expense in expenses:
                amount = expense.amount
                update_expense = expense
                update_expense.amount = userAmount
                update_expense.save()

                if expense.user != currentUser:

                    user_description = 'You owe ' + host.user.username + ' $' + str(userAmount) + ' for ' + expense.name
                    user_activity = GroupActivity.objects.create(
                        user = expense.user,
                        group = currentGroup,
                        expense = expense,
                        description = user_description,
                        general = 2,
                        validation = 2,
                        host = currentUser.username,
                    )


                    group_description = expense.user.username + ' owes ' + host.user.username + ' $' + str(userAmount) + ' for ' + expense.name
                    group_activity = GroupActivity.objects.create(
                        user = expense.user,
                        group = currentGroup,
                        expense = expense,
                        description = group_description,
                        general = 1,
                        validation = 2,
                        host = currentUser.username
                    )
                # if expense.user != host.user:
            return redirect('group_home', groupId = currentGroup.id)
    else:
        message = 'Please complete form below'
        form = UpdateExpenseEvenForm()
        parameters = {
            'message':message,
            'form':form,
            'currentGroup':currentGroup,
            'expenses':expenses,
        }
        return render(request, 'tabs/update_expense_even.html', parameters)

def updateExpenseIndividual(request, groupId, groupName):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    currentGroup = Group.objects.get(id = groupId)
    host = Member.objects.filter(group = groupId).filter(status = 2).first()
    expenses = Expense.objects.filter(group = currentGroup).filter(name = groupName).all()
    expenses_count = Expense.objects.filter(group = currentGroup).filter(name = groupName).count()
    SplitFormSet = formset_factory(UpdateExpenseIndividualForm, extra=expenses_count)
    # form_user = zip(expenses, SplitFormSet)
    if request.method == 'POST':
        formSet = SplitFormSet(request.POST)
        if 'tax' in request.POST:
            tax = request.POST['tax']
            amount = Decimal(tax)
            individual_tax = SplitEven(expenses_count, amount)
        if 'tip' in request.POST:
            tip = request.POST['tip']
            amount = Decimal(tip)
            individual_tip = SplitEven(expenses_count, amount)
        if formSet.is_valid():
            count = 0
            for form in formSet:
                cd = form.cleaned_data
                amount = cd['amount']
                description = cd['description']
                total_amount = amount + individual_tip + individual_tax
                expense = expenses[count]
                update_expense = expense
                update_expense.amount = total_amount
                update_expense.description = description
                update_expense.save()
                # if expense.user != host.user:

                user_description = 'You owe ' + host.user.username + ' $' + str(total_amount) + ' for ' + description
                group_description = expense.user.username + ' owe ' + host.user.username + ' $' + str(total_amount) + ' for ' + description

                user_activity = GroupActivity.objects.create(
                    user = expense.user,
                    group = currentGroup,
                    expense = expense,
                    description = user_description,
                    general = 2,
                    validation = 2,
                )

                group_activity = GroupActivity.objects.create(
                    user = expense.user,
                    group = currentGroup,
                    expense = expense,
                    description = group_description,
                    general = 1,
                    validation = 2,
                )

                count = count + 1
        return redirect('group_home', groupId = currentGroup.id)
    else:
        form = SplitFormSet()
        message = 'Please complete the form below'
        parameters = {
            'message':message,
            'form':form,
            'currentGroup':currentGroup,
            'expenses':expenses,
            # 'form_user':form_user,
        }
        return render(request, 'tabs/update_expense_individual.html', parameters)

def addExpenseSingle(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    friender = Friend.objects.filter(user = currentUser.username).all()
    friended = Friend.objects.filter(friend = currentUser).all()

    friends = friender | friended

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            location = cd['location']
            split = cd['split']
            reference = generateReferenceNumber()
            new_expense = Expense.objects.create(
                user = currentUser,
                name = name,
                location = location,
                split = split,
                reference = reference,
                created_by = currentUser.username,
            )
            description = 'You created a new expense: ' + new_expense.name + ' - ' + new_expense.location
            expense_activity = UserActivity.objects.create(
                user = currentUser,
                expense = new_expense,
                description = description,
                reference = reference,
            )
            for friend in friends:
                if friend.user == currentUser.username:
                    if friend.friend.username in request.POST:
                        new_expense = Expense.objects.create(
                             user = friend.friend,
                             name = name,
                             location = location,
                             split = split,
                             reference = reference,
                             created_by = currentUser.username,
                        )
                if friend.friend == currentUser:
                    if friend.user in request.POST:
                        friend = User.objects.get(username = friend.user)
                        new_expense = Expense.objects.create(
                             user = friend,
                             name = name,
                             location = location,
                             split = split,
                             reference = reference,
                             created_by = currentUser.username,
                        )
                description = currentUser.username + ' created a new expense: ' + new_expense.name + ' - ' + new_expense.location
                expense_activity = UserActivity.objects.create(
                    user = new_expense.user,
                    expense = new_expense,
                    description = description,
                    accepted = 1,
                    reference = reference
                )
        if split == 1:
            return redirect('update_expense_even_single', reference = reference)
        if split == 2:
            return redirect('update_expense_individual_single', reference = reference)

    else:
        form = ExpenseForm()
        message = 'Please fill out the form'
        parameters = {
            'form':form,
            'message':message,
            'friends':friends,
            'currentUser':currentUser,
        }
        return render(request, 'tabs/single_expense.html', parameters)

def updateExpenseEvenSingle(request, reference):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    expenses = Expense.objects.filter(reference = reference).all()
    expenses_count = Expense.objects.filter(reference = reference).count()
    host = currentUser
    if request.method == 'POST':
        form = UpdateExpenseEvenForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            amount = cd['amount']
            userAmount = SplitEven(expenses_count, amount)
            for expense in expenses:
                amount = expense.amount
                update_expense = expense
                update_expense.amount = userAmount
                update_expense.save()
                if expense.user != currentUser:
                    user_decription = 'You owe ' + host.username + ' $' + str(userAmount) + ' for ' + expense.name
                    user_activity = UserActivity.objects.create(
                        user = expense.user,
                        expense = expense,
                        description = user_decription,
                        accepted = 1,
                        status = 1,
                        reference = reference,
                        validation = 2,
                    )
            return redirect('user_expenses')
    else:
        message = 'Please complete the form '
        form = UpdateExpenseEvenForm()
        parameters = {
            'message':message,
            'form':form,
            'expenses':expenses,
        }
        return render(request, 'tabs/update_expense_even.html', parameters)

def updateExpenseIndividualSingle(request, reference):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    expenses = Expense.objects.filter(reference = reference)
    expenses_count = Expense.objects.filter(reference = reference).count()
    host = currentUser
    SplitFormSet = formset_factory(UpdateExpenseIndividualForm, extra=expenses_count)
    if request.method == 'POST':
        formSet = SplitFormSet(request.POST)
        if 'tax' in request.POST:
            tax = request.POST['tax']
            amount = Decimal(tax)
            individual_tax = SplitEven(expenses_count, amount)
        if 'tip' in request.POST:
            tip = request.POST['tip']
            amount = Decimal(tip)
            individual_tip = SplitEven(expenses_count, amount)
        if formSet.is_valid():
            count = 0
            for form in formSet:
                if form.is_valid:
                    cd = form.cleaned_data
                    amount = cd['amount']
                    description = cd['description']
                    total_amount = amount + individual_tip + individual_tax
                    expense = expenses[count]
                    if expense.user != currentUser:
                        update_expense = expense
                        update_expense.amount = total_amount
                        update_expense.description = description
                        update_expense.save()
                        user_description = 'You owe ' + host.username + ' $' + str(total_amount) + ' for ' + expense.name + ' - ' + description
                        user_activity = UserActivity.objects.create(
                            user = expense.user,
                            expense = expense,
                            description = user_description,
                            accepted = 1,
                            status = 1,
                            reference = reference,
                            validation = 2,
                        )
                count = count + 1
            return redirect('user_expenses')
    else:
        form = SplitFormSet()
        message = 'Please complete the form below'
        parameters = {
            'message':message,
            'form':form,
            'expenses':expenses,
            # 'form_user':form_user,
        }
        return render(request, 'tabs/update_expense_individual.html', parameters)

def verifyExpense(request, expenseId, activityId):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    currentExpense = Expense.objects.get(id = expenseId)
    currentExpense.status = 2
    currentExpense.save()

    currentActivity = GroupActivity.objects.get(id = activityId)
    activity_number = currentActivity.id + 1
    secondActivity = GroupActivity.objects.get(id = activity_number)

    host = currentActivity.host

    user_description = 'You transfered $' + str(currentExpense.amount) + ' to ' + host + ' for ' + currentExpense.description
    group_description = currentUser.username + ' transfered $' + str(currentExpense.amount) + ' to ' + host + ' for ' + currentExpense.description

    user_activity = GroupActivity.objects.create(
        user = currentUser,
        group = currentExpense.group,
        expense = currentExpense,
        description = user_description,
        general = 2
    )

    group_description = GroupActivity.objects.create(
        user = currentUser,
        group = currentExpense.group,
        expense = currentExpense,
        description = group_description,
        general = 1
    )

    currentActivity.delete()
    secondActivity.delete()

    group_id = currentExpense.group.id
    return redirect('group_home', group_id)

# the following is what will take care of the logout portion of the project
# this comment is to test and make sure that the new gitlab remote is working
def logoutPage(request):
    # the following 3 lines will check to see if there is a username in the session
    # which means that there is someone logged in and it will give them access to
    # opentab.
    if 'username' not in request.session:
        return redirect('login')
    else:
        # the following will dump the stored username in the session and redirect
        # to the login page.
        username = request.session['username']
        request.session.pop('username')
        return redirect('login')

def clearAllActivities(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    activities = UserActivity.objects.filter(user = currentUser).all()

    for activity in activities:
        update_activity = activity
        update_activity.status = 2
        update_activity.save()
    return redirect('user_home')

# the following is in charge of spliting an amount by number of people.
def SplitEven(count, amount):
    # the following will divide the amount passed though by the number of members
    # that was stored above.
    split_amount = amount/count
    # the following ensure that the result of the divide is rounded to 2 decimal
    # space.
    rounded_amount = round(split_amount, 2)
    return rounded_amount

def loggedInUser(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        return currentUser

def updateSessionUsername(request, new_username):
    if 'username' in request.session:
        request.session.pop('username')
        request.session['username'] = new_username
        return redirect('home_page')

# the view / method is called to generate a random number that is stored as the
# groups reference number for later use within the aaplication.
def generateReferenceNumber():
    reference = randint(1, 2147483646)
    return(reference)

def numberify(request, number):
    phone = '-'.join([number[:3], number[3:6], number[6:]])
    return phone

def setPrivacy(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    if currentProfile.privacy == 1:
        new_privacy = Privacy.objects.create(
            user = currentUser,
            groups = 1,
            friends = 1,
            expenses = 1,
            searchable = 1,
        )

    return new_privacy

def templateTesting(request):
    cheese = 'cheese'
    parameters = {
        'cheese':cheese,
    }
    return render(reqest, 'tabs/template_testing.html', parameters)

#--------------------------------------------------------------------------------
# the following is going to stay last because it is just used to view all records,
# not part of hte application core

# this is just a view that is used to display all of the differnet accounts and
# information that is stored in the database.
def accounts(request):
    # all of the objects in the database are grabbed to be displayed for testing
    # reason.
    groups = Group.objects.all()
    members = Member.objects.all()
    users = User.objects.all()
    privacies = Privacy.objects.all()
    requests = Request.objects.all()
    friends = Friend.objects.all()
    profiles = Profile.objects.all()
    expenses = Expense.objects.all()
    activities = Activity.objects.all()
    accounts = Accounts.objects.all()
    transfers = Transfers.objects.all()
    dwollas = Dwolla.objects.all()
    if 'username' in request.session:
        currentUser = request.session['username']
    else:
        currentUser = ''
    params = {
        'currentUser':currentUser,
        'groups':groups,
        'members':members,
        'users':users,
        'requests':requests,
        'friends':friends,
        'profiles':profiles,
        'expenses':expenses,
        'activities':activities,
        'accounts':accounts,
        'transfers':transfers,
        'dwollas':dwollas,
        'privacies':privacies,
    }
    return render(request, 'tabs/accounts.html', params)
    # return render(request, 'tabs/addMembers.html', params)

#-------------------------------------------------------------------------------
# all of the following methos in this section are going to be for the Dwolla integration
# api with opentab to create and initiate transfers between two users.
#-------------------------------------------------------------------------------

# the following method is going to be used to create a new user account within the
# Dwolla api system (sandbox/testing)
def createUserDwolla(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # the following is going to create the object that will store the new users
    # infromaiton and pass it with the request to the Deolla api in order to create
    # a new user within the api
    request_body = {
        'firstName':currentProfile.first_name,
        'lastName':currentProfile.last_name,
        'email':currentUser.email,
        'type':'personal',
        'address1':currentProfile.street,
        'city':currentProfile.city,
        'state':currentProfile.state,
        'postalCode':currentProfile.zip_code,
        'dateOfBirth':'1970-01-01',
        # 'ssn':ssn,
    }
    print(request_body)
    # the following lines will send the request to Dwolla and create a user within
    # the api. It will then return an object that can be displayed and grabed for
    # parsing of the information
    customer = app_token.post('customers', request_body)
    print(customer)
    # the following will grab the users location (url with id) and stores it in the
    # database for early retreival later on in the process
    customer.headers['location']
    customerLocation = customer.headers['location']
    print(customerLocation)

    # the following is going to take the new dwolla customer and grab the url locaiton
    # for the user. THe users locaiton is then stored in the local database for easy
    # retreival later in the application
    updateUser = currentProfile
    updateUser.dwolla_id = customerLocation
    updateUser.save()

# the following method is going to give yap the ability to retreive the users
# informaiton related to the dwolla api for dwolla actions
def searchUserDwolla(request):
    currentUser = loggedInUser(request)
    username = currentUser.username
    print(username)
    currentProfile = Profile.objects.get(user = currentUser)
    # the next two lines will grab the users dwolla app id so that the customer can
    # be retreived for useage
    customer_id = currentProfile.dwolla_id
    print(customer_id)
    customer = app_token.get(customer_id)
    # the following will print informaiton that iwas stored in the api to make
    # sure that the right information is retreived.
    return customer

# this method is where the user will be able to link an external bank account to the
# app and transfer money within the app from. I wrote this method to just test the
# transfer method. Once the Synapse API is up and running, this part will be automated
# and there is will be no need for this.
def linkAccount(request):
    currentUser = loggedInUser(request)
    # the following is a very simple and basic for processing section.
    if request.method == 'POST':
        form = LinkAccountForm(request.POST)
        # the following line is ogoing to check and make user that the form which
        # was submitted is valid before it the form is set to the processing method
        # at the bottom of the file.
        if form.is_valid():
            # the form and its content is sent to the Link Account method which will
            # take the informaiton that was submitted and process it through the Dwolla
            # api which will link a bank account to the users account
            linkAccountDwolla(request, form)
            return redirect('home_page')
    else:
        # the following will send the form to the html file where it will be filled
        # out and submitted for processing.
        form = LinkAccountForm()
        message = 'please fill out the entire form'
        parameters = {
            'form':form,
            'currentUser':currentUser,
            'message':message,
        }
        return render(request, 'tabs/link_account.html', parameters)

def linkAccountDwolla(request, form):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # before linking the account through the Dwolla api, the informaiton is collected
    # from the form that was submitted and stored
    cd = form.cleaned_data
    routing_number = cd['routingNumber']
    account_number = cd['accountNumber']
    account = cd['account']
    name = cd['accountName']
    # the users Dwolla id is pulled in order to link the account to the user
    customer_id = currentProfile.dwolla_id
    print(customer_id)
    # the content required to link and account through the api is stored in an object
    request_body = {
        'routingNumber':routing_number,
        'accountNumber':account_number,
        'type':account,
        'name':name,
    }
    # the new account is requested and sent to the api.
    source = app_token.post('%s/funding-sources' % customer_id, request_body)
    # the accounts id is pulled and stored in a variable before put in a local database
    sourceLocation = source.headers['location']
    print(sourceLocation)

    # the following is going to store the funding source link within the database
    # to make it easier to locate the funding source links later when making
    # transactions
    newFundingSource = Dwolla.objects.create(
        user = currentUser,
        source_name = name,
        source_id = sourceLocation
    )

# THe following will use the Dwolla api to retrieve all of hte different bank accounts
# that are connected and linked for the user that is logged in. This is accessable
# through the linked accounts file in the users home page
def linkedAccounts(request):
    # the following grabs the logged in user
    currentUser = loggedInUser(request)
    # the following will send the user through the account retreival method which
    # accesses the Dwolla table stored in the database which keeps the unique id
    # of every account that islinked
    accountsJson = listedLinkAccounts(request)
    accountsText = str(accountsJson)
    accounts = searchFundingSourcesDwolla(request, currentUser)
    print(accounts)
    # the following will check to see if there are in fact linked accounts connected
    # to the user. If there is no account, the user will be redirected to the page
    # where the user will be able to link a new account
    if accounts == None:
        message = 'There are no linked accounts - linkedAccounts'
        print(message)
        return redirect('link_account')
    # if there are accounts, they will be stored and passed to the html file where
    # the user will be able to view all accounts and set the default.
    for account in accounts:
        print(type(account.source_id))
    parameters = {
        'currentUser':currentUser,
        'accounts':accounts,
        'accountsText':accountsText,
    }
    return render(request, 'tabs/linked_accounts.html', parameters)

# the following method is going to be used to enable the user to set a default
# account that will be automatically used during transacitons for quick and easy
# processing. It can also be changed here as well
def setDefaultSource(request, source_id):
    currentUser = loggedInUser(request)
    # the following will grab all of the accounts linked to the user
    sources = Dwolla.objects.filter(user = currentUser).all()
    # the following wil grab the account that the user has selected to become the
    # defauly account
    currentSource = Dwolla.objects.get(id = source_id)

    # the for statment will gp through every account coonected to the user for processing
    for source in sources:
        # the following if statement will check to see if there is apreviously set
        # default account
        if source.status == 2:
            # if there is a defauly account which is not the one selected, then the
            # newly selected account will become the new default account and the only
            # default will become a non-default account
            if source.id != currentSource.id:
                # the follownig 3 lines will set the new defauly acocunt by updating
                # the record.
                updated_source = currentSource
                updated_source.status = 2
                updated_source.save()
                # the following will take the old default and make it a normal account
                un_default_source = source
                un_default_source.status = 1
                un_default_source.save()
                return redirect('linked_accounts')
    if currentSource.status ==1:
        update_source = currentSource
        update_source.status = 2
        update_source.save()

    return redirect('linked_accounts')

def searchFundingSourcesDwolla(request, user):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # the following will grab the selected user whose funding sources are being searched
    selected_user = user
    print(selected_user)
    # the following is an alternative for searching through the dwolla api in order
    # to grab all of the links related to the users funding sources
    sources = Dwolla.objects.filter(user = selected_user).all()
    print(sources)
    # the following will check to see if there are any currently linked sources with the user
    if sources == None:
        # if there are no sources,  the user will be sent to the link bank account page
        # to link a bank account
        message = 'You have no linked accounts'
        print(message)
        return redirect('link_account')
    # if there are sources linked with the user selected, the sources will be scanned and
    # all of the sources will be retured to the method call
    for source in sources:
        name = source.source_name
        _id = source.source_id
        print(name)
        print(_id)
    return sources

def findDefaultSource(request, user):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    defaults = Dwolla.objects.filter(user = user).all()
    if defaults == None:
        return defaults
    if defaults != None:
        for default in defaults:
            if default.status == 2:
                userDefault = default
                return userDefault
            else:
                userDefault = Dwolla.objects.filter(user = user).first()
                return userDefault

def createTransactionDwolla(request, sender, receiver, amount, description, group_id):
    # cheese = 'cheese'
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    senderMessage = 'sender = ' + str(sender.username)
    receiverMessage = 'receiver = ' + str(receiver.username)
    print(senderMessage)
    print(receiverMessage)

    senderSource = findDefaultSource(request, sender)
    if senderSource == None:
        if sender == currentUser:
            message = 'logged in user does not have account'
            failure = 'current user'
            print(message)
            return failure
        if sender != currentUser:
            message = 'non logged in user has no account'
            failure = 'non user'
            print(message)
            return failure
    if senderSource:
        message = 'sender has default account set'
        print(message)
        sender_id = senderSource.source_id
        print(sender_id)

    receiverSources = Dwolla.objects.filter(user = receiver).all()
    for source in receiverSources:
        if source.status == 2:
            message = 'default account is set'
            print(message)
            receiver_id = source.source_id
            print(receiver_id)

    paymentId = generateReferenceNumber()

    print(paymentId)

    request_body = {
      '_links': {
        'source': {
          'href': str(sender_id)
        },
        'destination': {
          'href': str(receiver_id)
        }
      },
      'amount': {
        'currency': 'USD',
        'value': str(amount)
      },
      'metadata': {
        'paymentId': str(paymentId),
        'note': str(description)
      },
      'clearing': {
        'destination': 'next-available'
      },
      'correlationId': '8a2cdc8d-629d-4a24-98ac-40b735229fe2'
    }

    print(request_body)

    transfer = app_token.post('transfers', request_body)
    transfer.headers['location']

def templateTesting(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    parameters = {
        'currentUser':currentUser,
        'currentProfile':currentProfile,
    }

    return render(request, 'tabs/template_testing.html', parameters)

#-------------------------------------------------------------------------------
# all of the following have to deal with the synpase api integration with the
# opentab api as a means to transfer money between bank account to bank account
#-------------------------------------------------------------------------------

# the following is going to create a new user within the Syanpse added which is needed
#in order to keep refernce of each user as well as the accounts and transfers that are
# processed later on
def createUserSynapse(request):
    # the following grabs the current suer and profile for the current user which
    # will be used to retrieve and update informaiton pretaining to the new user
    currentUser = loggedInUser(request)
    profile= Profile.objects.get(user = currentUser)

    # the following saves a reference to the current profile
    currentProfile = profile
    # the following lines will store inforaiton that is sent with the new user
    # request rather than enter it directly to the arguments
    legal_name = currentProfile.first_name + " " + currentProfile.last_name
    note = legal_name + " has just created his synapse profile "
    supp_id = generateReferenceNumber()
    cip_tag = currentUser.id
    # the following is all of the information that is required in order to make a
    # new user within the Synapse application
    args = {
        'email':str(currentUser.email),
        'phone_number':str(currentProfile.phone),
        'legal_name':str(legal_name),
        'note': str(note),
        'supp_id':str(supp_id),
        'is_business':False,
        'cip_tag':cip_tag,
    }
    # the following is the request to the synapse api as well as the returned
    # json that contains information that needs to ba saved in local database
    create_user = SynapseUser.create(client, **args)
    response = create_user.json
    # the following updates the current profile to add the users synapse id within
    # the local database.
    if response:
        synapse_id = response['_id']
        updateProfile = currentProfile
        updateProfile.synapse_id = synapse_id
        updateProfile.save()

# the following method is where the current user will go to retreive their synapse
# account informaiton in order to make other synapse requests.
def retreiveUserSynapse(request):
    # the following is going to be where the record for the logged in user is grabed
    # as well as the profile.
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # the following is the current users Synapse Id required for calling the API
    user_id = currentProfile.synapse_id
    # the following will make a synapse request which will return the users
    # account informaiton in a json format
    searchedUser = SynapseUser.by_id(client, str(user_id))
    # the folloiwng will check to make sure there is object returned before returning
    # it to the method call.
    if searchedUser:
        print(searcheduser)
        return searchedUser

# The following is the first part of the linking your bank account through login
# to your bank account. This will grab the form and pass it in order to complete
# the linking bank accounts processing.
def loginAccountSynapse(request):
    # the following willl check and make sure that there is a user that is logged in
    # and grab their profile.
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # the following is going to grab the form that is submitted and process the form
    if request.method == 'POST':
        # the followig will grab the form from the POST
        form = LinkAccountSynapse(request.POST)
        # this will make sure that the form values are valid. If they are valid,
        # the form will be sent to a processing method that will complete the
        # processing
        if form.is_valid():
            authorizeLoginSynapse(request, form)
            return redirect('home_page')
    # if there was no form submitted, the following is where the form will be
    # rendered with other additional information that is needed.
    else:
        form = LinkAccountSynapse()
        message = "Enter you bank login credentials"
        parameters = {
            'form':form,
            'message':message,
            'currentUser':currentUser
        }
        return render(request, 'tabs/link_account_synapse.html', parameters)

# the followig method is going to do the full processing of the linkig bank account
# form and complete the request action.
def authorizeLoginSynapse(request, form):
    # this will grab the currently logged in user and the users profile for later
    # reference
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # the following grabs the logged in users synapse id from his profile.
    user_id = currentProfile.synapse_id
    # the following will send a request to get the users synapse profile from the
    # api and later user that response object.
    synapseUser = SynapseUser.by_id(client, str(user_id))
    print(synapseUser)
    # the following section is going to be the informaiton passed from the form that
    # was submitted, commented out for testing
    # cd = form.cleaned_data
    # bank_code = cd['bank_code']
    # bank_id = cd['bank_id']
    # bank_pw = cd['bank_password']
    # the following are just testing values in sandbox to make sure the processing
    # works and is able to send the request and receive the response to process
    bank_id = 'synapse_good'
    bank_pw = 'test1234'
    bank_code = 'fake'
    print(bank_code)
    print(bank_id)
    print(bank_pw)
    # the following is the object that is going to be passed with the response
    args = {
        'bank_name':bank_code,
        'username':bank_id,
        'password':bank_pw,
    }
    print(args)
    # the followig is the actual request that will process the request and return
    # a response that will then be verified
    ach_us = AchUsNode.create_via_bank_login(synapseUser, **args)
    # the following will check to see if mfa verification is needed for the specified
    # bank
    verification = ach_us.mfa_verified
    print(verification)
    # If the mfa verification is needed, the following will simply verify the account
    # and make the account verified.
    if verification == False:
        ach_us.mfa_message
        nodes = ach_us.answer_mfa('test_answer')
        ach_us.mfa_verified
    print(ach_us)


# the following method is going to be where all of the users synapse nodes will be
# requested and processed
def listedLinkAccounts(request):
    # the following grabs the currenly logged in users record and profile within
    # the application
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # the following will grab the users synapse id from the users local profile.
    user_id = currentProfile.synapse_id
    print(user_id)
    # the following will grab the entire synapse profile by sending an api request
    # with the users synapse profile.
    synapseUser = SynapseUser.by_id(client, str(user_id))
    # the following are options for how to display and structure the response for
    # all of the different nodes linked to the users account
    options = {
        'page':1,
        'per_page':20,
        'type': 'ACH-US',
    }
    # the following is the request and response with all of the users linked nodes
    # ready to be processed and storage of certain information.
    nodes = Node.all(synapseUser, **options)
    for node in nodes:
        print (node)
        print (type(node))

    parameters = {
        'currentUser':currentUser,
        'user_id':user_id,
        'nodes':nodes,
    }

    return render(request, 'tabs/linked_accounts_synapse.html', parameters)

def createTransaction(request):
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    user_id = currentProfile.synapse_id
    synapseUser = SynapseUser.by_id(client, str(user_id))
    print(synapseUser)

    node = Node.by_id(synapseUser, '59d16cd56d7d8a002f763df7')
    print(node)
    args = {
        'to_type': 'ACH-US',
        'to_id': '59d012da6d7d8a002f756e83',
        'amount': 32.05,
        'currency': 'USD',
        'ip': '127.0.0.1',
        'process_in': 0, # delay until processing (in days) [optional]
        'note': 'hi synapse', # a note to synapse [optional]
        'supp_id': 'ABC123', # optional
    }

    transaction = Transaction.create(node, **args)
    print(transaction)

    return transaction

# within the following view method, this will allow the user to create a transfer of money
# between the user's linked external bank account though Synapse and the synpase sub-account
# that will hold the money that is usable within the application... It will take that transfer
# and create a record for each transfer within the activity table and the balance table
def transfers(request):
    currentUser = loggedInUser(request)
    # the following grabs all the profiles that will be used later on in the method.
    # THe profile is where the users in app balance is stored and updated, We grab all
    # of the records so that later in the method, we can check and see if they logged in
    # user has an existing profile, or if there is a new to create a new profile to store
    # the users balance.
    profiles = Profile.objects.all()
    # the following is simple form processing where the information collected from the form
    # is stored in variables.
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            main = cd['main']
            transfer = cd['transfer']
            amount = cd['amount']
            memo = cd['memo']
            # the following is a new transfer object that stored the transfer within the database
            new_transfer = Transfers.objects.create(
                user = currentUser,
                main = main,
                transfer = transfer,
                amount = amount,
                memo = memo,
                frequency = 1,
                status = 1,
            )
            # this is where the profile proccessing is happening...
            # the forst for statement will go through each profile and see if the current
            # user has a profile, if there is a profile, then it is stored in a variable for
            # later use
            for profile in profiles:
                if profile.user.username == currentUser.username:
                    currentProfile = profile
            # the following will  take the current profile of the user and check a few
            # parameters to execute neccessary code
            if currentProfile:
                # the following is going to grab the currently saved balance that exists
                # within the users profile balance
                balance = currentProfile.balance
                # the following two if statments, will check to see if money is being
                # transfered to or from the tabz account or linked bank account.
                # if it is going to the tabz account, the users overall app balance will
                # up by adding current balance with amount specified. The opposite goes for
                # money being transfered out of the Tabz account
                if main == 'Tabz':
                    currentProfile.balance = balance - amount
                    currentProfile.save()
                    message = 'You have transfered ' + str(amount) + ' from your Tabz account to main account'
                if transfer == 'Tabz':
                    currentProfile.balance = balance + amount
                    currentProfile.save()
                    message = 'You have transfered ' + str(amount) + ' from your main account to Tabz account'
                # the following is the new activity record that is created after every single
                # transfer that goes on. THis allows the user to see exactly what kind
                # of transfer happened and details about that transfer in the activity section
                new_activity = Activity.objects.create(
                    user = currentUser,
                    description = message,
                    status = 1,
                    category = 1,
                )
            return redirect('home_page')
    else:
        # this is the processing that goes on if the form was not submitted. this is where
        # everything is passed to the form page.
        form = TransferForm()
        message = 'please fill out the below form'
        parameters = {
            'form':form,
            'currentUser':currentUser,
            'message':message,
        }
        return render(request, 'tabs/user_balance.html', parameters)
