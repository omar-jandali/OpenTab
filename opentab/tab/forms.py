# a lot of the database tables that I created and you build models of dont
# actually need a form for the user to input informaiton to. The only tables
# that i think need to be created are the following...
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    
# Validates password agaisnt validators defined in settings
def pass_val(word):
    validators.validate_password(password=word)


# Checks username for uniquness and length
def unique_username(username):
    if len(username) < 6:
        raise ValidationError(
            _('Must be at least 6 characters.')
        )
    else:
        u = User.objects.filter(username=username).exists()
        if u:
            raise ValidationError(
                _('Username is already taken.')
            )


# Checks email for uniqueness (bootstrap will check format)
def unique_email(email):
    u = User.objects.filter(email=email).exists()
    if u:
        raise ValidationError(
            _('Email has already been registered.')
        )


class SignupForm(forms.Form):
    f_name = forms.CharField(label='First Name', max_length=50)
    l_name = forms.CharField(label='Last Name', max_length=50)
    username = forms.CharField(label='Username',
                               max_length=50,
                               validators=[unique_username])
    password = forms.CharField(label='Password',
                               max_length=50,
                               validators=[pass_val])
    verify = forms.CharField(label='Verify Password', max_length=50)
    email = forms.EmailField(label='Email',
                             max_length=50,
                             validators=[unique_email])

    # Validates that passwords match
    def clean_password2(self):
        data = self.cleaned_data
        if 'password' in data:
            if data['password'] != data['password2']:
                self._errors["password2"] = self.error_class(
                    ['Passwords do not match.'])
        return data
