from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from random import randint

from .models import Group, User, Member
from .forms import CreateGroupForm, AddMembersForm

# the following def is going to be what grabs all of the different groups that
# are in the database
# filters can be added later

def groups(request):
    # following is all of th actions that are taken after the form is submitted
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        referenceCode = generateReferenceNumber()
        if form.is_valid():
            cd = form.cleaned_data
            groupName = cd['name']
            groupDescription = cd['description']
            groupDefaultCreatedBy = User.objects.get(username='hanijandali')
            new_group = form.save(commit=False)
            new_group.name = groupName
            new_group.description = groupDescription
            new_group.reference_code = referenceCode
            new_group.created_by = groupDefaultCreatedBy
            new_group.save()
            new_member = Member.objects.create(
                user = groupDefaultCreatedBy,
                group_reference = referenceCode,
                status = 1,
            )
            #return redirect('/tab/addMembers')
            return HttpResponseRedirect(reverse('add_members', args=[groupName]))
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

def addMembers(request, groupName):
    currentUser = User.objects.get(username='hanijandali')
    currentGroup = Group.objects.filter(created_by=currentUser).get(name=groupName)
    if request.method == "POST":
        form = AddMembersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = cd['user']
            new_member = Member.objects.create(
                user = user,
                group_reference = currentGroup.reference_code,
                status = 1,
            )
            return redirect('/tab/accounts')
    else:
        addMembers = AddMembersForm()
        message = 'add members below'
        params = {
            'addMembers':addMembers,
            'message':message,
            'currentGroup':currentGroup,
        }
    return render(request, 'tabs/add_members.html', params)

def accounts(request):
    groups = Group.objects.all()
    members = Member.objects.all()
    params = {
        'groups':groups,
        'members':members,
    }
    return render(request, 'tabs/accounts.html', params)
    # return render(request, 'tabs/addMembers.html', params)

def generateReferenceNumber():
    reference = randint(1, 2147483646)
    return(reference)
