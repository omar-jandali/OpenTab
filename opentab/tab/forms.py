# a lot of the database tables that I created and you build models of dont
# actually need a form for the user to input informaiton to. The only tables
# that i think need to be created are the following...
from django import forms
from django.forms import ModelForm
from tab.models import Group, Member, Record, Transaction

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(max_length=22)
    password = forms.CharField(max_length=22, widget=forms.PasswordInput)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=22)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)
    verify = forms.CharField(max_length=16, widget=forms.PasswordInput)
    email = forms.EmailField(max_length=50)

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
        fields = ['description', 'split']

class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'user']

class EvenSplitTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']
    # amount = forms.DecimalField(label='Total Amount', decimal_places=2, max_digits=9)
    # description = forms.CharField(max_length=250)

class IndividualSplitTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']
