from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from random import randint

from .models import Group, User, Member, Record, Transaction
from .forms import CreateGroupForm, AddMembersForm, AddRecordForm, AddTransactionForm
from .forms import SignupForm, LoginForm

def signup(request):
    if request.method == 'GET':
        params = {}
        return render(request, 'tab/signup.html', params)
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            print('form validated')
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User(first_name=f_name,
                        last_name=l_name,
                        username=username,
                        email=email)
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Account Created!')
            return redirect('login')
        else:
            print('form is not valid')
            params = {}
            params['form'] = form
            return render(request, 'tab/signup.html', params)


def login_page(request):
    if request.method == 'GET':
        return render(request, 'tab/login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in username:
                u = User.objects.filter(email=username).first()
                if u:
                    user = authenticate(request, username=u.username, password=password)
                else:
                    user = None
            else:
                user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('logged_in')
        print('no user')
        context = {}
        context['error'] = 'Username or password is incorrect'
        return render(request, 'tab/login.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required
def logged_in(request):
    print('user is logged in')
    s = "<h1>Logged in as {} {}</h1>".format(request.user.first_name, request.user.last_name)
    s += "<br><a href='http://127.0.0.1:8000/logout'>logout</a>"
    return HttpResponse(s)

# The following view is what will be used to display all of the groups and informaiton
# for the logged in user including groups balances and friends
# Passed in var:
#   name = the name of the user that is logged in
def userHome(request, name):
    # the database object for the user that is selected
    currentUser = User.objects.get(username=name)
    # this is used to grab all of the groups that the user is a part of
    members = Member.objects.filter(user=currentUser).all()
    # this is used to actually display the group info that the user is a part of
    groups = Group.objects.all()
    #these are all the parameters that need to be passed to the html tempalte
    parameters = {
        'currentUser':currentUser,
        'members':members,
        'groups':groups
    }
    return render(request, 'tabs/user_home.html', parameters)

# The following is the view that will manage the groups profile. It will be the main
# page that users will be able to use to find all of the different information
# regarding the specific group that is selected.
# Passed in var:
# groupId = the id of the group that is selected (will be changed to the group name
# later into the development)
def groupHome(request, groupId):
    # the following is the group object with the id that is passed in the url
    group = Group.objects.get(id=groupId)
    # the following are all of the members that are in the databse
    members = Member.objects.all()
    records = Record.objects.all()
    #these are all the parameters that need to be passed to the html tempalte
    parameters = {
        'group':group,
        'members':members,
        'records':records,
    }
    return render(request, 'tabs/group_home.html', parameters)

# The view is g0ing to be used to create the group and add the information for the
# group before creating the record in the database. It will also be incharge of adding
# the first memeber to the group (the person who created the group).
#
#  will redirect to the adding memeber view (need to be fixed)
def groups(request):
    # the following is the user objectr of the person who is creating the group
    user = User.objects.get(username='omar')
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
            # the new_member instance is create and saaved that will add the first
            # member of the group which is the person that created the group
            new_member = Member.objects.create(
                user = user,
                group = new_group,
                status = 1,
            )
            return redirect('/tab/accounts')
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
    # the following two lines grab the users object for the current user as well as
    # the group object related to the id that was passed in
    currentUser = User.objects.get(username='omar')
    group = Group.objects.get(id=groupId)
    # the form is similar to the form submition above for reference
    if request.method == "POST":
        form = AddMembersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = cd['user']
            valid_user = User.objects.get(username=user)
            new_member = Member.objects.create(
                user = valid_user,
                group = group,
                status = 1,
            )
            # the followin three lines will grab the group that the user is adding
            # a member to and updating the groups count by one every time a new user
            # is added to the group
            update_group = Group.objects.get(id=groupId)
            update_group.count = update_group.count + 1
            update_group.save()
            return redirect('/tab/accounts')
    else:
        # the form and users objects are passed to the form. This is because instead
        # of typing in a username, it is easier to have a list of all the user objects
        # in a scollable input form and just click on who the new person is
        form = AddMembersForm()
        users = User.objects.all()
        message = 'add members below'
        params = {
            'form':form,
            'message':message,
            'group':group,
        }
    return render(request, 'tabs/add_members.html', params)

# This view is what will be in charge of adding the different types of records to
# the group and keeping track of all the expense amounts and dealing with the splitting
# of the expense.
def addRecord(request, groupId):
    # for the records, the user and group need to be provided to know what group
    # this record is attached to and who created the record.
    user = User.objects.get(username='omar')
    group = Group.objects.get(id=groupId)
    # the followin process is similar to the form validation for the group view.
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            split = cd['split']
            new_record = Record.objects.create(
                status = 1,
                split = split,
                group = group,
                user = user,
            )
            return redirect('/tab/accounts')
    else:
        # the only tyhing that needed to be passed was the group to display the naem
        # and the form that is going to be used and filled out by the user and submitted
        form = AddRecordForm()
        message = 'fill out the form to add a record'
        parameters = {
            'group':group,
            'form':form,
            'message':message,
        }
    return render(request, 'tabs/add_record.html', parameters)

# This is the view that is going to be manage the creation of different
# transactions that are going to be used to track how much money each person is
# paying for each record
def addTransaction(request, groupId, recordId):
    user = User.objects.get(username='omar')
    group = Group.objects.get(id=groupId)
    record = Record.objects.get(id=recordId)
    if request.method == 'POST':
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            amount = cd['amount']
            description = cd['description']
            new_transaction = Transaction.objects.create(
                amount = amount,
                description = description,
                group = group,
                user = user,
                record = record,
            )
            return redirect('tab/accounts')
    else:
        form = AddTransactionForm()
        message = 'fill out the form below'
        parameters = {
            'record':record,
            'form':form,
            'message':message
        }
    return render(request, 'tabs/add_transactions.html', parameters)

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
    params = {
        'groups':groups,
        'members':members,
        'users':users,
        'records':records,
        'transactions':transactions,
    }
    return render(request, 'tabs/accounts.html', params)
    # return render(request, 'tabs/addMembers.html', params)

def accountsDelete(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        Groups.objects.all().remove()
        return redirect('/tab/accounts')
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
