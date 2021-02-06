from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from accounts.models import UserProfile
from django.contrib import messages
from accounts.forms import CreateUserForm, UserProfileForm
from django.urls import reverse
from . import forms

def index(request):
    return render(request, 'index.html')

def user_signup(request):
    registered = False

    if request.method == 'POST':
        user_form = CreateUserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user=user     # one to one relationship
            
            if 'profile_pic' in request.FILES:
                print('profile pic is uploaded by {}'.format(user.username))
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        
        else:
            print(user_form.errors,profile_form.errors)
    
    else:
        user_form = CreateUserForm()
        profile_form = UserProfileForm()

    return render(request,'accounts/registration.html',
                            {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('<h1>Your account is not active</h1>')
        else:
            # return messages.error(request, "Error")
            print('Someone tried to login with username = {} and password = {}'.format(username, password))
            return HttpResponse('<h1> Invalid username and password</h1>')
    else:
        return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'index.html')