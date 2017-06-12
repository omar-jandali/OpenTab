from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth.models import User


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
    # else:
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = request.POST['username']
    #         password = request.POST['password']
    #         user = authenticate(request, username=username, password=password)
    #         if user:
    #             login(request, user)
    #             return redirect('profile')
    #     print('no user')
    #     context = {}
    #     context['error'] = 'Username or password is incorrect'
    #     return somewhere
