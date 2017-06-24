# a lot of the database tables that I created and you build models of dont
# actually need a form for the user to input informaiton to. The only tables
# that i think need to be created are the following...
from django import forms
from django.forms import ModelForm
from tab.models import Group, Member

member_count_choices = (('bronze', '1-4',),
                        ('silver', '5-7',),
                        ('gold', '8-10',),
                        ('platnium', '11+',))

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class AddMembersForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user']
# class AddMembersForm(forms.ModelForm):
#     class Meta:
