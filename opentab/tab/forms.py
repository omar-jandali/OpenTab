# a lot of the database tables that I created and you build models of dont
# actually need a form for the user to input informaiton to. The only tables
# that i think need to be created are the following...
from django import forms

class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=25)
    description = forms.CharField(max_length=200)
    image = fomrs.ImageField()
    member_count = forms.IntegerField()

class AddMembersFourForm(forms.Form):
    user_one = forms.CharField(max_length = 25)
    user_two = forms.CharField(max_length = 25)
    user_three = forms.CharField(max_length = 25)
    user_four = forms.CharField(max_length = 25)

class AddMembersSevenForm(forms.Form):
    user_one = forms.CharField(max_length = 25)
    user_two = forms.CharField(max_length = 25)
    user_three = forms.CharField(max_length = 25)
    user_four = forms.CharField(max_length = 25)
    user_five = forms.CharField(max_length = 25)
    user_sex = forms.CharField(max_length = 25)
    user_seven = forms.CharField(max_length = 25)

class AddMembersTenForm(forms.Form):
    user_one = forms.CharField(max_length = 25)
    user_two = forms.CharField(max_length = 25)
    user_three = forms.CharField(max_length = 25)
    user_four = forms.CharField(max_length = 25)
    user_five = forms.CharField(max_length = 25)
    user_sex = forms.CharField(max_length = 25)
    user_seven = forms.CharField(max_length = 25)
    user_eight = forms.CharField(max_length = 25)
    user_nine = forms.CharField(max_length = 25)
    user_ten = forms.CharField(max_length = 25)

class AddMembersElevenForm(forms.Form):
    user_one = forms.CharField(max_length = 25)
    user_two = forms.CharField(max_length = 25)
    user_three = forms.CharField(max_length = 25)
    user_four = forms.CharField(max_length = 25)
    user_five = forms.CharField(max_length = 25)
    user_sex = forms.CharField(max_length = 25)
    user_seven = forms.CharField(max_length = 25)
    user_eight = forms.CharField(max_length = 25)
    user_nine = forms.CharField(max_length = 25)
    user_ten = forms.CharField(max_length = 25)
    user_eleven = forms.CharField(max_length = 25)

class CreateRecordForm(forms.Form):
    amount = forms.FloatField()
    description = fomrs.CharField(max_length = 200)
    type = forms.IntegerField()
