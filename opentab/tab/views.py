from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


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
            messages.add_message(request, messages.SUCCESS, 'Account Created!')
            return redirect('login')
        else:
            print('form is not valid')
            params = {}
            params['form'] = form
            return render(request, 'tab/signup.html', params)


def login_page(request):
    if request.method == 'GET':
        return render(request, 'tab/login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in username:
                u = User.objects.filter(email=username).first()
                if u:
                    user = authenticate(request, username=u.username, password=password)
                else:
                    user = None
            else:
                user = authenticate(request, username=username, password=password)
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
    print('user is logged in')
    s = "<h1>Logged in as {} {}</h1>".format(request.user.first_name, request.user.last_name)
    s += "<br><a href='http://127.0.0.1:8000/logout'>logout</a>"
    return HttpResponse(s)
