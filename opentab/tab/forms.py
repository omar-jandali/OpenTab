# a lot of the database tables that I created and you build models of dont
# actually need a form for the user to input informaiton to. The only tables
# that i think need to be created are the following...
from django import forms
from django.forms import ModelForm
from tab.models import Group, Member, Record

split_bill_choices = (('1', 'even',),
                      ('2', 'individual',))

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class AddMembersForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user']

class AddRecordForm(forms.ModelForm):
    split_choices = (('1', 'even'),
                     ('2', 'individual'))
    split = forms.TypedChoiceField(
        choices=split_choices, widget=forms.RadioSelect, coerce=int
    )
    class Meta:
        model = Record
        fields = ['amount', 'description', 'split']
