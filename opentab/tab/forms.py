# a lot of the database tables that I created and you build models of dont
# actually need a form for the user to input informaiton to. The only tables
# that i think need to be created are the following...
from django import forms

class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=25)
    description = forms.CharField(max_length=200)
    image = fomrs.ImageField()
    member_count = forms.IntegerField()

class CreateRecordForm(forms.Form):
    amount = forms.FloatField()
    description = fomrs.CharField(max_length = 200)
    type = forms.IntegerField()
