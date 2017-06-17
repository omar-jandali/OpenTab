from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
import os
from django.template.loader import get_template
from itsdangerous import URLSafeTimedSerializer


TOKEN_KEY = 'Debug_mode_only'
TOKEN_SALT = 'Change_in_production'
EMAIL_CONFIRM_WEB_LINK = 'http://127.0.0.1:8000'


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(TOKEN_KEY)
    return serializer.dumps(email, salt=TOKEN_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(TOKEN_KEY)
    try:
        email = serializer.loads(
            token,
            salt=TOKEN_SALT,
            max_age=expiration
        )
    except Exception as e:
        print(e)
        return False
    return email


# Cannot be used for more than one person
def send_email(to_add, subject, content, context):
    html_file = 'email/{}.html'.format(content)
    txt_file = 'email/{}.txt'.format(content)
    html_template = get_template(html_file)
    txt_template = get_template(txt_file)
    html_content = html_template.render(context)
    txt_content = txt_template.render(context)
    email = requests.post(
        "https://api.mailgun.net/v3/gabelwright.com/messages",
        auth=("api", "key-c3a7aee2c1b68f154153164394af11e9"),
        data={"from": "notification@gabelwright.com",
              "to": to_add,
              "subject": subject,
              "text": txt_content,
              "html": html_content})
    print(email)
    return email


def send_confirm_email(email):
    token = generate_confirmation_token(email)
    link = EMAIL_CONFIRM_WEB_LINK + reverse('confirm_email', args=[token])
    print(link)
    context = {'link': link}
    send_email(email, 'Confirm Email', 'confirm_email', context)


def signup(request):
    if request.method == 'GET':
        params = {}
        return render(request, 'tab/signup.html', params)
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            print('form validated')
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User(first_name=f_name,
                        last_name=l_name,
                        username=username,
                        email=email)
            user.set_password(password)
            user.save()
            send_confirm_email(user.email)
            profile = Profile(user=user)
            profile.save()
            messages.add_message(request, messages.SUCCESS, 'Account Created!')
            return redirect('login')
        else:
            print('form is not valid')
            params = {}
            params['form'] = form
            return render(request, 'tab/signup.html', params)


def confirm_email(request, token):
    if request.method == 'GET':
        email = confirm_token(token)
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                profile = Profile.objects.filter(user=user).first()
                profile.confirmed_email = True
                profile.save()
                messages.add_message(
                    request, messages.SUCCESS, 'Email Confirmed!')
                return redirect('profile')
        messages.add_message(
            request, messages.ERROR, 'Email could not be confirmed. '
                                     'Link is either invalid or expired.')
        return redirect('profile')


def login_page(request):
    if request.method == 'GET':
        return render(request, 'tab/login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            u = User.objects.filter(
                Q(username=username) | Q(email=username)).first()
            if u:
                user = authenticate(
                    request, username=u.username, password=password)
                if user:
                    login(request, user)
                    return redirect('logged_in')
        print('no user')
        context = {}
        context['error'] = 'Username or password is incorrect'
        return render(request, 'tab/login.html', context)


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required
def logged_in(request):
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        profile = Profile(user=request.user)
        profile.save()
    print('user is logged in')
    return render(request, 'tab/profile.html')
