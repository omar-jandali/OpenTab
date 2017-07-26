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

from .models import Group, User, Member, Record, Transaction, Request, Friend
from .forms import CreateGroupForm, AddMembersForm, AddRecordForm, AddTransactionForm
from .forms import SignupForm, LoginForm, EvenSplitTransactionForm
from .forms import IndividualSplitTransactionForm, SignupForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            verify = cd['verify']
            email = cd['email']
            if password == verify:
                new_user = User.objects.create(
                    username = username,
                    password = password,
                    email = email,
                )
                request.session['username'] = username
                return redirect('accounts')
            else:
                message = 'Password and Verify dont match'
                parameters = {
                    'form':form,
                    'message':message,
                }
                return render(request, 'tabs/signup.html', parameters)
    else:
        form = SignupForm()
        message = 'Fill out the form'
        parameters = {
            'form':form,
            'message':message,
        }
        return render(request, 'tabs/signup.html', parameters)

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user:
                request.session['username'] = username
                return redirect('home_page')
            else:
                message = 'invalid login info'
                parameters = {
                    'message':message,
                    'form':form,
                }
            return render(request, 'tabs/login.html', parameters)
    else:
        form = LoginForm()
        message = 'Login Below'
        parameters = {
            'form':form,
            'message':message,
        }
        return render(request, 'tabs/login.html', parameters)

def logout_page(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        request.session.pop('username')
        return redirect('login')

# The following view is what will be used to display all of the groups and informaiton
# for the logged in user including groups balances and friends
# Passed in var:
#   name = the name of the user that is logged in
def userHome(request):
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
        if request.method == "POST":
            for searched in request.POST:
                searched = request.POST['searched']
                users = User.objects.all()
                for user in users:
                    if searched == user.username:
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

def sendRequest(request, requested):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        requestedUser = User.objects.get(username = requested)
        new_request = Request.objects.create(
            user = currentUser,
            requested = requestedUser,
        )
        return redirect('accounts')

def acceptRequest(request, accepted):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        acceptedUser = User.objects.get(username = accepted)
        new_friend = Friend.objects.create(
            user = currentUser,
            friend = acceptedUser,
            category = 1,
            status = 1,
        )
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
        groups = Group.objects.filter(id = groupId).all()
        members = Member.objects.filter(user = currentUser).all()
        for member in members:
            for group in groups:
                if group.id == member.group.id:
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
                # if friend.username in request.POST:
                #     # user that is currently selected will be passed and then passed into
                #     # the new record that is created for every selected member
                #     selected_user = User.objects.get(username = user.username)
                #     new_member = Member.objects.create(
                #         user = selected_user,
                #         group = group,
                #         status = 1,
                #     )
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
                            new_transaction = Transaction.objects.create(
                                amount = 0.00,
                                description = description,
                                group = group,
                                user = selected_user,
                                record = new_record,
                            )
                        if new_record.split == 2:
                            new_transaction = Transaction.objects.create(
                                amount = 0.00,
                                description = 'expense',
                                group = group,
                                user = selected_user,
                                record = new_record,
                            )
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
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        group = Group.objects.get(id=groupId)
        record = Record.objects.get(id=recordId)
        transCount = Transaction.objects.filter(record=recordId).all().count()
        print(transCount)
        transactions = Transaction.objects.filter(record=recordId).all()
        SplitFormSet = formset_factory(IndividualSplitTransactionForm, extra=transCount)
        if request.method == 'POST':
            if record.split == 1:
                form = EvenSplitTransactionForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    amount = cd['amount']
                    description = cd['description']
                    split_amount = SplitEven(record, amount)
                    for trans in transactions:
                        if trans.record.id == record.id:
                            trans.description = description
                            trans.amount = split_amount
                            trans.save()
                    return redirect('group_home', groupId=group.id)
            if record.split == 2:
                formset = SplitFormSet(request.POST)
                if 'tax' in request.POST:
                    tax = request.POST['tax']
                    amount = Decimal(tax)
                    taxSplit = SplitEven(record, amount)
                else:
                    taxSplit = 0
                if 'tip' in request.POST:
                    tip = request.POST['tip']
                    amount = Decimal(tip)
                    tipSplit = SplitEven(record, amount)
                else:
                    tipSplit = 0
                if formset.is_valid():
                    i=0
                    for form in formset:
                        cd = form.cleaned_data
                        currentAmount = cd['amount']
                        currentDescription = cd['description']
                        finalAmount = currentAmount + taxSplit + tipSplit
                        print(currentAmount)
                        print(currentDescription)
                        currentTrans = transactions[i]
                        currentTrans.amount = finalAmount
                        currentTrans.description = currentDescription
                        currentTrans.save()
                        print(currentTrans)
                        i = i + 1
                        #---------------------------------
                        # this is where I want to iterate through the query results and
                        # assign the correct appropriate inutes to the appropriate user
                        #---------------------------------
            return redirect('accounts')
        else:
            if record.split == 1:
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

def SplitEven(record, amount):
    record_count = record.count
    print(type(record_count))
    print(record_count)
    print(type(amount))
    print(amount)
    split_amount = amount/record_count
    print(split_amount)
    rounded_amount = round(split_amount, 2)
    print (record_count)
    print (amount)
    print (split_amount)
    return rounded_amount
