from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import formset_factory
from django.db.models import Q

from random import randint
from decimal import Decimal

from .models import Group, User, Member, Record, Transaction, Request, Friend, Profile
from .forms import CreateGroupForm, AddMembersForm, AddRecordForm, AddTransactionForm
from .forms import SignupForm, LoginForm, EvenSplitTransactionForm
from .forms import IndividualSplitTransactionForm, SignupForm, LoginForm, ProfileForm
from .forms import UserBalance

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
                new_user = User.objects.create(
                    username = username,
                    password = password,
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
def login_page(request):
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
                return redirect('home_page')
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

# the following is what will take care of the logout portion of the project
def logout_page(request):
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

# The following view is what will be used to display all of the groups and informaiton
# for the logged in user including groups balances and friends
# Passed in var:
#   name = the name of the user that is logged in
def userHome(request):
    # the following 2 lines will check to see if there is a username in the session
    # which means that there is someone logged in and it will give them access to
    # opentab.
    if 'username' in request.session:
        username = request.session['username']
        # the database object for the user that is selected
        currentUser = User.objects.get(username=username)
        # this is used to grab all of the groups that the user is a part of
        members = Member.objects.filter(user=currentUser).all()
        # the following are what will be used ot get all of the user requests
        requester = Request.objects.filter(user = username).all()
        requested = Request.objects.filter(requested = currentUser).all()
        # the following are what will be used to grab all of your firends
        friender = Friend.objects.filter(user = username).all()
        friended = Friend.objects.filter(friend = currentUser).all()
        # this is used to actually display the group info that the user is a part of
        groups = Group.objects.all()
        # the following post request is what will process the searched portion of
        # the home page.
        if request.method == "POST":
            for searched in request.POST:
                # the following stores the name that was seached in the search box
                searched = request.POST['searched']
                # the following will create an object with all of the users
                users = User.objects.all()
                # the following will go thorugh each user in the database.
                for user in users:
                    # the following if statement will check to see if the name
                    # that was searched exists in the database.
                    if searched == user.username:
                        # if the name exists in the database, the user will be stored
                        # in the searchedUser variable and passed to the html page
                        # and displayed for the user.
                        searchedUser = user
                        message = 'results for: ' + user.username
                        parameters = {
                            'currentUser':currentUser,
                            'members':members,
                            'groups':groups,
                            'searchedUser':searchedUser,
                            'message':message,
                            'requester':requester,
                            'requested':requested,
                            'friender':friender,
                            'friended':friended,
                        }
                        return render(request, 'tabs/user_home.html', parameters)
                    else:
                        # if the user does not exist in the database, an erorr message
                        # with show up to let the loged in user that there is no one
                        # with the entered username
                        message = 'the user does not exist'
                        parameters = {
                            'currentUser':currentUser,
                            'members':members,
                            'groups':groups,
                            'message':message,
                            'requester':requester,
                            'requested':requested,
                            'friender':friender,
                            'friended':friended,
                        }
                return render(request, 'tabs/user_home.html', parameters)
        else:
            # the following will display all relavent inforomation excluding the
            # search results.
            parameters = {
                'currentUser':currentUser,
                'members':members,
                'groups':groups,
                'requester':requester,
                'requested':requested,
                'friender':friender,
                'friended':friended,
            }
            return render(request, 'tabs/user_home.html', parameters)
    else:
        return redirect('login')

# The following is the view that will manage the groups profile. It will be the main
# page that users will be able to use to find all of the different information
# regarding the specific group that is selected.
# Passed in var:
# groupId = the id of the group that is selected (will be changed to the group name
# later into the development)
def groupHome(request, groupId):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        group = Member.objects.filter(user = currentUser).filter(group = groupId).first()
        # the following is the group object with the id that is passed in the url
        # group = Group.objects.get(name = groupName)
        members = Member.objects.filter(group = group.group).all()
        records = Record.objects.filter(group = group.group).all()
        transactions = Transaction.objects.filter(group = group.group).all()
        #these are all the parameters that need to be passed to the html tempalte
        parameters = {
            'members':members,
            'records':records,
            'group':group,
            'transactions':transactions,
        }
        return render(request, 'tabs/group_home.html', parameters)

def profile_setup(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            print(form)
            if form.is_valid():
                cd = form.cleaned_data
                age = cd['age']
                print(age)
                city = cd['city']
                print(city)
                phone = cd['phone']
                print(phone)
                privacy = cd['privacy']
                print(privacy)
                new_profile = Profile.objects.create(
                    user = currentUser,
                    age = age,
                    city = city,
                    phone = phone,
                    privacy = privacy,
                )
                return redirect('accounts')
        else:
            form = ProfileForm()
            message = 'fill out form below'
            parameters = {
                'form':form,
                'currentUser':currentUser,
                'message':message,
            }
            return render(request, 'tabs/profile_setup.html', parameters)

def userBalance(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        if request.method == 'POST':
            form = UserBalance(request.POST)
            cd = form.cleaned_data
            cheese = 'cheese'
        else:
            form = UserBalance()
            message = 'please fill out the form below'
            parameters = {
                'form':form,
                'currentUser':currentUser,
                'message':message,
            }
            return render(request, 'tabs/user_balance.html', parameters)

# the following method managed the sending of friend requests to other users and
# storing a record of that in the database.
def sendRequest(request, requested):
    # the following 3 lines will check to see if there is a username in the session
    # which means that there is someone logged in and it will give them access to
    # opentab.
    if 'username' not in request.session:
        return redirect('login')
    else:
        # the following line grabs the loggedin user object os that it can be passed
        # into the database with the correct informaiton.
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        # the following will grab the user object with the username that was submitted
        # for the friend request.
        requestedUser = User.objects.get(username = requested)
        # the following created a new record in the request table within the database.
        new_request = Request.objects.create(
            user = currentUser,
            requested = requestedUser,
        )
        return redirect('accounts')

# The following method will process the acceptaance of a friend request.
def acceptRequest(request, accepted):
    # the following 3 lines will check to see if there is a username in the session
    # which means that there is someone logged in and it will give them access to
    # opentab.
    if 'username' not in request.session:
        return redirect('login')
    else:
        # when a user accepts a friend request, the logged in user and the user
        # attached to the friend request will be stored in variables.
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        acceptedUser = User.objects.get(username = accepted)
        # a new record will be added to the Friend table in teh database that will
        # be later used as a way to display all of a users friends.
        new_friend = Friend.objects.create(
            user = currentUser,
            friend = acceptedUser,
            category = 1,
            status = 1,
        )
        # after the new friend record is created, the original request is found
        # and deleted so that they request does not keep showing up on the logged in
        # users home page.
        requests = Request.objects.filter(requested = currentUser).all()
        for request in requests:
            if request.user == acceptedUser.username:
                request.delete()
        return redirect('accounts')

# The view is g0ing to be used to create the group and add the information for the
# group before creating the record in the database. It will also be incharge of adding
# the first memeber to the group (the person who created the group).

#  will redirect to the adding memeber view (need to be fixed)
def createGroup(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        currentUser = request.session['username']
        # the following is the user objectr of the person who is creating the group
        user = User.objects.get(username=currentUser)
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
                    created_by = user,
                )
                #---------------------------------------------------------
                # create a column that addes the person who created the group
                #---------------------------------------------------------
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

# This view is what will add different members to the gorup that is selected. This
# method will be in charge of not only adding the member to the group and keeping
# a record of it in the database, but also keep track of the number of members in
# the group so that it is easily calculated later.
# Passed in var:
#   groupId - the id of the group that the memeber will be added to.
def addMembers(request, groupId):
    if 'username' not in request.session:
        return redirect('login')
    else:
        # the following two lines grab the users object for the current user as well as
        # the group object related to the id that was passed in
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        # the following line will grab the group object that members will be added ot and
        # stored in a variable that will be referenced later.
        groups = Group.objects.filter(id = groupId).all()
        # the following will grab all of the member objects that are related to the logged
        # in user.
        members = Member.objects.filter(user = currentUser).all()
        for member in members:
            for group in groups:
                if group.id == member.group.id:
                    # if the groups id is the same as the group id that is stored in the
                    # members object, the currently cycled through group is stored as group
                    group = Group.objects.get(id = group.id)
        users = User.objects.all()
        friends = Friend.objects.all()
        # the form is similar to the form submition above for reference
        if request.method == "POST":
            # the following will scroll through every user in the users table
            new_default_member = Member.objects.create(
                user = currentUser,
                group = group,
                status = 1,
            )
            for friend in friends:
                # it will then check to see if the usersname was returned in the request.
                # if the username was checked, it will be returned, otherwise it will not
                # be passed.
                if friend.user == currentUser.username:
                    selected_user = User.objects.get(username = friend.friend.username)
                    new_member = Member.objects.create(
                        user = selected_user,
                        group = group,
                        status = 1,
                    )
                if friend.friend.username == currentUser.username:
                    selected_user = User.objects.get(username = friend.user)
                    print(selected_user)
                    new_member = Member.objects.create(
                        user = selected_user,
                        group = group,
                        status = 1,
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

# This view is what will be in charge of adding the different types of records to
# the group and keeping track of all the expense amounts and dealing with the splitting
# of the expense.
def addRecord(request, groupId):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        selectedGroup = Member.objects.filter(user = currentUser).filter(group = groupId).first()
        group = Group.objects.get(id = selectedGroup.group.id)
        members = Member.objects.filter(group=group)
        # the followin process is similar to the form validation for the group view.
        if request.method == 'POST':
            message = 'process'
            form = AddRecordForm(request.POST)
            # the following will take the form that is based on the records model in the
            # forms.py file. It will only process the split port on the html file.
            # The record members will be processed below.
            if form.is_valid():
                cd = form.cleaned_data
                split = cd['split']
                description = cd['description']
                new_record = Record.objects.create(
                    description = description,
                    split = split,
                    count = 0,
                    status = 1,
                    group = group,
                    user = currentUser,
                )
                # the following will take all of the members in the group and for each
                # member, it will go through and check to see if the if the checkbox
                # for the specific user is selected.
                for member in members:
                    # if the user was selected, then the username would appear in the
                    # POST request. If the user was not selected, it would not appear
                    # in the POST request.
                    if member.user.username in request.POST:
                        # if the member is in the request, it will find the members user
                        # recor in the database and use it to create the new transaciton
                        # history.
                        selected_user = User.objects.get(username = member.user.username)
                        # this is the new transaction record.
                        if new_record.split == 1:
                            # there are two version of the new transaction record with one
                            # difference. If it is an even split or 1, then the description
                            # is going to be whatever description the user writes for the
                            # related expense
                            new_transaction = Transaction.objects.create(
                                amount = 0.00,
                                description = description,
                                group = group,
                                user = selected_user,
                                record = new_record,
                            )
                        if new_record.split == 2:
                            # if the record is an idividual split, then a predetermined
                            # string will be stored and later changed when the users inputs
                            # each individual description in the add transaction method below
                            new_transaction = Transaction.objects.create(
                                amount = 0.00,
                                description = 'expense',
                                group = group,
                                user = selected_user,
                                record = new_record,
                            )
                        # the following few lines will grab the record that is created and
                        # for every member that was added to the group, there is a counter
                        # that will keep track of the number of people involed in the specific
                        # record.
                        update_record = new_record
                        update_record.count = update_record.count + 1
                        update_record.save()
                return redirect('add_transactions', groupId=group.id, recordId=new_record.id)

        else:
            # the only tyhing that needed to be passed was the group to display the naem
            # and the form that is going to be used and filled out by the user and submitted
            form = AddRecordForm()
            message = 'no processing'
            params = {
                'group':group,
                'members':members,
                'form':form,
                'message':message,
            }
        return render(request, 'tabs/add_records.html', params)

# This is the view that is going to be manage the creation of different
# transactions that are going to be used to track how much money each person is
# paying for each record
def addTransaction(request, groupId, recordId):
    # the following 3 lines will check to see if there is a username in the session
    # which means that there is someone logged in and it will give them access to
    # opentab.
    if 'username' not in request.session:
        return redirect('login')
    else:
        # the following two lines will grab the user that is logged in and grab
        # the logged in users object from the database.
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        # the group related to the transactions is selected and stored in a variable
        group = Group.objects.get(id=groupId)
        # the record related to the transactions is selected and stored in a variable
        record = Record.objects.get(id=recordId)
        # the following will just grab the amount of people that are involved in the
        # spefic transacton and record.
        transCount = Transaction.objects.filter(record=recordId).all().count()
        print(transCount)
        # the following grabs all of the objects that are related to this specific
        # transaction and record.
        transactions = Transaction.objects.filter(record=recordId).all()
        # the following will create a formset that will create a form for rach of the
        # members that are directly related to the transaction. the number of forms
        # comes from the result of the transCount queryset
        SplitFormSet = formset_factory(IndividualSplitTransactionForm, extra=transCount)
        if request.method == 'POST':
            # once the form is submitted, if there was an even split expense, it is
            # proccessed below.
            if record.split == 1:
                # the will grab all of the form content and validate it as well as
                # make sure that the method is working with cleaned data
                form = EvenSplitTransactionForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    # the amount and description for the transaction are stored below
                    amount = cd['amount']
                    description = cd['description']
                    # the folllowing is a call to a method at the bottom of the file
                    # which will take the totla amount of money related to the expense
                    # as well as the number of people involved in the transaction.
                    # The method that is called will divide the amount bt number to
                    # determine how much every person is responsible for
                    split_amount = SplitEven(record, amount)
                    for trans in transactions:
                        if trans.record.id == record.id:
                            # in teh following lines all of the existing trnasaciton
                            # record will be updated to include the correct amount due
                            # as well as the description that was submitted for the
                            # specific transaction.
                            trans.description = description
                            trans.amount = split_amount
                            trans.save()
                    return redirect('group_home', groupId=group.id)
            if record.split == 2:
                # if the user maked the expense as an individual expense, there is
                # more procesing that needs to be done which is below.
                formset = SplitFormSet(request.POST)
                # the first step is to grab the tax and the user submitted and divide
                # that amount by the number of users in the transaction.
                if 'tax' in request.POST:
                    tax = request.POST['tax']
                    amount = Decimal(tax)
                    # the following is the amount of money that each person will be
                    # responsible for before adding it to each  person total
                    taxSplit = SplitEven(record, amount)
                else:
                    # similar to the above statment, the tip that is submitted by the
                    # user is divided evenly between the number of people in the
                    # transaction before it is added to the total amount each person
                    # is responsible for.
                    taxSplit = 0
                if 'tip' in request.POST:
                    tip = request.POST['tip']
                    amount = Decimal(tip)
                    tipSplit = SplitEven(record, amount)
                else:
                    tipSplit = 0
                # the following will validate the entire formset to make sure the
                # the content of the form is all valide
                if formset.is_valid():
                    # a default value is set here because it is how the processing is
                    # done in the below section - to be more specific how each member
                    # of the transaction is given the correct amount and description
                    # is assigned.
                    i=0
                    # this will go through  each for in the formset and process each
                    # form individually
                    for form in formset:
                        # the following will clean the data for each form and grab
                        # the inputted amount and description.
                        cd = form.cleaned_data
                        currentAmount = cd['amount']
                        currentDescription = cd['description']
                        # the total amount that the current user must pay is added
                        # up below and stored before the transaction record is updated.
                        finalAmount = currentAmount + taxSplit + tipSplit
                        print(currentAmount)
                        print(currentDescription)
                        # the following line is what will be used to keep track of the
                        # currently selected user will be store and updated. This is
                        # also what will make sure that the form within the cycle is synced
                        # with the appropriate users transaction object.
                        currentTrans = transactions[i]
                        # the current transaction object with the correct user is updated
                        # with the new amount and description before it is saved.
                        currentTrans.amount = finalAmount
                        currentTrans.description = currentDescription
                        currentTrans.save()
                        print(currentTrans)
                        # the following will increment each time the loop is cycled so that
                        # it is not just one transaction record that is constantly being updated
                        i = i + 1
                        #---------------------------------
                        # this is where I want to iterate through the query results and
                        # assign the correct appropriate inutes to the appropriate user
                        #---------------------------------
            return redirect('accounts')
        else:
            if record.split == 1:
                # if the record is an even split, the correct form is passed thorugh
                form = EvenSplitTransactionForm()
                message = 'fill out the form below'
                parameters = {
                    'record':record,
                    'form':form,
                    'message':message,
                    'transactions':transactions,
                }
                return render(request, 'tabs/add_even_transactions.html', parameters)
            if record.split == 2:
                # if the indivual record was selected, the correct formset is passed
                # through for the user to fill out.
                print(SplitFormSet)
                message = 'message'
                parameters = {
                    'record':record,
                    'SplitFormSet':SplitFormSet,
                    'message':message,
                    'transactions':transactions,
                }
                return render(request, 'tabs/add_individual_transaction.html', parameters)

# this is just a view that is used to display all of the differnet accounts and
# information that is stored in the database.
def accounts(request):
    # all of the objects in the database are grabbed to be displayed for testing
    # reason.
    groups = Group.objects.all()
    members = Member.objects.all()
    users = User.objects.all()
    records = Record.objects.all()
    transactions = Transaction.objects.all()
    requests = Request.objects.all()
    friends = Friend.objects.all()
    profiles = Profile.objects.all()
    if 'username' in request.session:
        currentUser = request.session['username']
    else:
        currentUser = ''
    params = {
        'currentUser':currentUser,
        'groups':groups,
        'members':members,
        'users':users,
        'records':records,
        'transactions':transactions,
        'requests':requests,
        'friends':friends,
        'profiles':profiles,
    }
    return render(request, 'tabs/accounts.html', params)
    # return render(request, 'tabs/addMembers.html', params)

def accountsDelete(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        Groups.objects.all().remove()
        return redirect('/accounts')
    else:
        message = 'delete all of the following records'
        params = {
            'groups':groups,
            'message':message,
        }
        return render(request, 'tabs/delete_accounts.html', params)

# the view / method is called to generate a random number that is stored as the
# groups reference number for later use within the aaplication.
def generateReferenceNumber():
    reference = randint(1, 2147483646)
    return(reference)

# the following is in charge of spliting an amount by number of people.
def SplitEven(record, amount):
    # this will take the count number that is tracked with in teh reocrds objects
    # ever time a new member is added to the record.
    record_count = record.count
    # the following will divide the amount passed though by the number of members
    # that was stored above.
    split_amount = amount/record_count
    # the following ensure that the result of the divide is rounded to 2 decimal
    # space.
    rounded_amount = round(split_amount, 2)
    return rounded_amount
