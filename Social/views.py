from django.contrib.auth.models import User, auth
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
    
def logout(request):
    auth.logout(request)
    return redirect('index')