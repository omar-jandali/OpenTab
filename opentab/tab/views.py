from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction

from random import randint

from .models import Group, User, Member
from .forms import CreateGroupForm

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
            # new_member.user = groupDefaultCreatedBy
            # new_member.group_reference = referenceCode
            # new_member.status = 1
            # new_member.save()
            return redirect('/tab/accounts')

    else:
        # the following is the storing of the forms
        createGroup = CreateGroupForm()
        message = ''
    # the following are all the objects that are going to be passed to the
    # rendering remplate
    parameters = {
        "creategroup" : createGroup,
        "message" : message,
    }
    return render(request, 'tabs/create_group.html', parameters)

def addMembers(request):

    return render(request, 'tabs/accounts', params)

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
