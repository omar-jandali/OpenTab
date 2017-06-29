from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from random import randint

from .models import Group, User, Member, Record
from .forms import CreateGroupForm, AddMembersForm, AddRecordForm

# the following def is going to be what grabs all of the different groups that
# are in the database
# filters can be added later

def userHome(request, name):
    currentUser = User.objects.get(username=name)
    members = Member.objects.filter(user=currentUser).all()
    groups = Group.objects.all()
    parameters = {
        'currentUser':currentUser,
        'members':members,
        'groups':groups
    }
    return render(request, 'tabs/user_home.html', parameters)

def groupHome(request, groupName):
    currentUser = User.objects.get(username='hanijandali')
    userGroups = Member.objects.filter(user=currentUser).all()
    members = Member.objects.all()
    groups = Group.objects.filter(name=groupName).all()
    parameters = {
        'userGroups':userGroups,
        'groups':groups,
        'groupName':groupName,
        'members':members,
    }
    return render(request, 'tabs/group_home.html', parameters)


def groups(request):
    # following is all of th actions that are taken after the form is submitted
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        referenceCode = generateReferenceNumber()
        user = User.objects.get(username='omar')
        if form.is_valid():
            cd = form.cleaned_data
            groupName = cd['name']
            groupDescription = cd['description']
            new_group = form.save(commit=False)
            new_group.name = groupName
            new_group.description = groupDescription
            new_group.reference_code = referenceCode
            new_group.created_by = user.username
            new_group.save()
            new_member = Member.objects.create(
                user = user,
                group = new_group,
                status = 1,
            )
            return redirect('/tab/accounts')
            #return redirect(reverse('add_members', args=[new_group.id]))
    else:
        # the following is the storing of the forms
        createGroup = CreateGroupForm()
        message = 'enter group info below'
    # the following are all the objects that are going to be passed to the
    # rendering remplate
    parameters = {
        "creategroup" : createGroup,
        "message" : message,
    }
    return render(request, 'tabs/create_group.html', parameters)

def addMembers(request, groupId):
    currentUser = User.objects.get(username='omar')
    group = Group.objects.get(id=groupId)
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
            update_group = Group.objects.get(id=groupId)
            update_group.count = update_group.count + 1
            update_group.save()
            return redirect('/tab/accounts')
    else:
        addMembers = AddMembersForm()
        users = User.objects.all()
        message = 'add members below'
        params = {
            'addMembers':addMembers,
            'message':message,
            'group':group,
        }
    return render(request, 'tabs/add_members.html', params)

def addRecord(request, groupId):
    user = User.objects.get(username='omar')
    group = Group.objects.get(id=groupId)
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            amount = cd['amount']
            description = cd['description']
            split = cd['split']
            new_record = Record.objects.create(
                amount = amount,
                description = description,
                status = 1,
                split = split,
                group = group,
                user = user,
            )
            return redirect('/tab/accounts')
    else:
        form = AddRecordForm()
        message = 'fill out the form to add a record'
        parameters = {
            'group':group,
            'form':form,
            'message':message,
        }
    return render(request, 'tabs/add_record.html', parameters)

def accounts(request):
    groups = Group.objects.all()
    members = Member.objects.all()
    users = User.objects.all()
    records = Record.objects.all()
    params = {
        'groups':groups,
        'members':members,
        'users':users,
        'records':records,
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

def generateReferenceNumber():
    reference = randint(1, 2147483646)
    return(reference)
