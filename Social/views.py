from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        twitsForm= TwitForm(request.POST or None)
        if request.method == "POST":
            if twitsForm.is_valid():
                twit= twitsForm.save(commit= False)
                twit.user= request.user
                twit.save()
                messages.success(request, ('You twit has been posted'))
                return redirect('index')
        twits= Twit.objects.all().order_by('-twit_date')
        context= {
            'twits': twits,
            'form': twitsForm,
        }
        return render(request, 'index.html', context= context)
    else:
        twits= Twit.objects.all().order_by('-twit_date')
        context= {
            'twits': twits,
        }
        return render(request, 'index.html', context= context)

def profileList(request):
    if request.user.is_authenticated:
        profile= UserProfile.objects.exclude(user= request.user)
        context= {
            'profiles': profile,
        }
        return render(request, 'profileList.html', context= context)
    else: 
        messages.success(request, ('You must be logged in to view this page...'))
        return redirect('index')

def profile(request,username):
    if request.user.is_authenticated:
        userr = User.objects.get(username=username)
        profile= UserProfile.objects.get(user= userr)
        cuntUser= UserProfile.objects.get(user= User.objects.get(username=request.user))
        myTwits= Twit.objects.filter(user= userr).order_by('-twit_date')

        if request.method == "POST":
            if request.POST.get('follow'):
                cuntUser.follows.add(profile)
                # return redirect('profile', username=username)
            elif request.POST.get('unfollow'):
                cuntUser.follows.remove(profile)
                # return redirect('profile', username=username)
            cuntUser.save()

        context= {
            'user_profile': profile,
            'user': cuntUser.follows.all,
            'mytwits': myTwits,
        }
        return render(request, 'profile.html', context= context)
    else:
        messages.success(request, ('You must be logged in to view this page...'))
        return redirect('index')

def login_user(request):
    if request.method == 'POST':
        username= request.POST['username']
        userpassword= request.POST['userpassword']
        user= authenticate(request, username= username, password= userpassword)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in...'))
            return redirect('index')
        else:
            messages.success(request, ('There was an error logging in. Please try again...'))
            return redirect('sign in')
    else:
        context= {

        }
        return render(request, 'login.html', context= context)

def signup(request):
    form= SignUpForm()
    if request.method == 'POST':
        form= SignUpForm(request.POST)
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password1']
        confpassword= request.POST['password2']
        if User.objects.filter(username= username).exists():
            messages.success(request, ('Username already exist...'))
            return redirect('sign up')
        elif User.objects.filter(email= email).exists():
            messages.success(request, ('Email already exist...'))
            return redirect('sign up')
        elif password != confpassword:
            messages.success(request, ('Password doesn\'t match...'))
            return redirect('sign up')
        else:
            if form.is_valid():
                form.save()
                username= form.cleaned_data['username']
                password= form.cleaned_data['password1']
                first_name= form.cleaned_data['first_name']
                last_name= form.cleaned_data['last_name']
                email= form.cleaned_data['email']
                print(username, password, first_name, last_name, email, 'data')
                user= authenticate(username= username, password= password)
                login(request, user)
                messages.success(request, (f'You are welcome to Twitty {username}...'))
                return redirect('index')
            else:
                messages.success(request, ('Password is weak, it should be at least 8 character\'s and it can\'t be entirely numeric...'))
                return redirect('sign up')
    context= {
        'form': form, 
    }
    return render(request, 'signup.html', context= context)

def updateProfile(request):
    context={
        
    }
    return render(request, 'updateProfile.html', context= context)

def logout_user(request):
    auth.logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('index')