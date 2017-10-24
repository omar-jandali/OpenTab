# a lot of the database tables that I created and you build models of dont
# actually need a form for the user to input informaiton to. The only tables
# that i think need to be created are the following...
from django import forms
from django.forms import ModelForm, extras
from tab.models import Group, Member, Profile, User, Privacy
from tab.models import Transfers, Accounts, Expense

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

bank_code_choices = (('ally', 'Ally Bank'),
                     ('altra', 'Altra Federal Credit Union'),
                     ('arvest', 'Associated Bank'),
                     ('associatedbank', 'Altra Federal Credit Union'),
                     ('bangor', 'Altra Federal Credit Union'),
                     ('bbt', 'Altra Federal Credit Union'),
                     ('bcu', 'Altra Federal Credit Union'),
                     ('becu', 'Altra Federal Credit Union'),
                     ('bfsfcu', 'BankFund Staff Federal Credit Union'),
                     ('bofa', 'Bank of America'),
                     ('boftw', 'Bank of the West'),
                     ('capone', 'Capital One'),
                     ('capone360', 'Capital One 360'),
                     ('centralillinois', 'Central Bank Illinois'),
                     ('chase', 'Chase'),
                     ('citi', 'Citibank'),
                     ('citizens', 'Citizens Bank'),
                     ('cuone', 'Credit Union One (MI)'),
                     ('desertschoolsfcu', 'Desert Schools Federal Credit Union'),
                     ('empowerfcu', 'Empower Federal Credit Union'),
                     ('fidelity', 'Fidelity'),
                     ('fifththird', 'Fifth Third Bank'),
                     ('firsthawaiian', 'First Hawaiian Bank'),
                     ('firstrepublic', 'First Republic Bank'),
                     ('firsttennessee', 'First Tennessee'),
                     ('frostbank', 'Frost Bank'),
                     ('georgiasowncu', 'Georgia\'s Own Credit Union'),
                     ('gobank', 'GoBank'),
                     ('golden1cu', 'Golden 1 Credit Union'),
                     ('hsbc', 'HSBC Bank'),
                     ('huntington', 'Huntington Bank'),
                     ('kembafcu', 'Kemba Financial Credit Union'),
                     ('keybank', 'Key bank'),
                     ('mtb', 'M&T Bank'),
                     ('ncsecu', 'NC State Employees Credit Union'),
                     ('nevadastate', 'Nevada State Bank'),
                     ('nfcu', 'Navy Federal Credit Union'),
                     ('pnc', 'PNC Bank'),
                     ('regions', 'Regions'),
                     ('santander', 'Santander Bank'),
                     ('schoolsfcu', 'Schools Financial Credit Union'),
                     ('schwab', 'Charles Schwab'),
                     ('simple', 'Simple'),
                     ('suntrust', 'SunTrust Bank'),
                     ('svb', 'Silicon Valley Bank'),
                     ('synchrony', 'Synchrony Bank'),
                     ('td', 'TD Bank'),
                     ('tdbusiness', 'TD Bank BusinessDirect'),
                     ('union', 'Union Bank'),
                     ('us', 'US Bank'),
                     ('usaa', 'USAA'),
                     ('wells', 'Wells Fargo'),
                     )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=22)
    password = forms.CharField(max_length=22, widget=forms.PasswordInput)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=22)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)
    verify = forms.CharField(max_length=16, widget=forms.PasswordInput)
    email = forms.EmailField(max_length=50)

class ProfileForm(forms.ModelForm):
    split_choices = (('1', 'public'),
                     ('2', 'private'))
    privacy = forms.TypedChoiceField(
        choices=split_choices, widget=forms.RadioSelect, coerce=int
    )
    dob = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'dob', 'street', 'city', 'state',
                    'zip_code', 'phone', 'privacy']

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class AddMembersForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user']

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserSettingsTwoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, label="First Name")
    last_name = forms.CharField(max_length=20, label="Last Name")
    class Meta:
        model = Profile
        fields = ['bio', 'first_name', 'last_name']

class UpdatePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=20, label="Current password", widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=20, label="New password", widget=forms.PasswordInput)
    verify_password = forms.CharField(max_length=20, label="Verify password", widget=forms.PasswordInput)

class UpdateInfoForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Profile
        fields = ['phone', 'dob', 'street', 'city', 'state', 'zip_code']

class UpdatePrivacyForm(forms.ModelForm):
    privacy_choices = (('1', 'Everyone'),
                       ('2', 'Friends'),
                       ('3', 'Only Me'))
    friends = forms.TypedChoiceField(
        label="Friends", choices=privacy_choices
    )
    groups = forms.TypedChoiceField(
        label="Friends", choices=privacy_choices
    )
    expenses = forms.TypedChoiceField(
        label="Friends", choices=privacy_choices
    )
    searchable = forms.TypedChoiceField(
        label="Friends", choices=privacy_choices
    )
    class Meta:
        model = Privacy
        fields = ['friends', 'groups', 'expenses', 'searchable']

# the following are for the new type of expense system that is going to be added
#------------------------------------------------------------------------------
class ExpenseForm(forms.ModelForm):
    split_choices = (('1', 'even'),
                      ('2', 'individual'))
    split = forms.TypedChoiceField(
        choices=split_choices, widget=forms.RadioSelect, coerce=int
    )
    class Meta:
        model = Expense
        fields = ['name', 'location', 'split']

class UpdateExpenseEvenForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount']


class UpdateExpenseIndividualForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description']

#------------------------------------------------------------------------------

class TransferForm(forms.ModelForm):
    acct_choices = (('Tabz', 'Tabz - Username'),
                    ('Wells Fargo', 'Wells Fargo - Username'))
    main = forms.TypedChoiceField(
        choices=acct_choices
    )
    transfer = forms.TypedChoiceField(
        choices=acct_choices
    )
    class Meta:
        model = Transfers
        fields = ['main', 'transfer', 'amount', 'memo']

class LinkAccountForm(forms.Form):
    account_choices = (('checking', 'Checking'),
                       ('savings', 'Savings'))
    account = forms.TypedChoiceField(
        choices = account_choices
    )
    accountName = forms.CharField(
        max_length=100, label="Account Name"
    )
    routingNumber = forms.CharField(max_length=22, label="Routing Number")
    accountNumber = forms.CharField(max_length=22, label="Account Number")


class LinkAccountSynapse(forms.Form):
    bank_code = forms.TypedChoiceField(choices=bank_code_choices)
    bank_id = forms.CharField(max_length=100, label="Bank Username")
    bank_password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label="Bank Password")
