from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
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
                messages.success(request, (f'You have started following {username}...'))
            elif request.POST.get('unfollow'):
                cuntUser.follows.remove(profile)
                messages.success(request, (f'You have successfully unfollowed {username}...'))
            cuntUser.save()
            return redirect(request.META.get('HTTP_REFERER'))
        username_followers_id= []
        for users_followers in profile.follows.all():
            username_followers_id.append(users_followers.id)

        context= {
            'user_profile': profile,
            'user_profile_ids': username_followers_id,
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
        if form.is_valid():
            form.save()
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            first_name= form.cleaned_data['first_name']
            last_name= form.cleaned_data['last_name']
            email= form.cleaned_data['email']
            user= authenticate(username= username, password= password)
            login(request, user)
            messages.success(request, (f'You are welcome to Twitty {username}...'))
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.success(request, (f"Error: {error}"))
            return redirect('sign up')
    context= {
        'form': form, 
    }
    return render(request, 'signup.html', context= context)

def updateProfile(request):
    if request.user.is_authenticated:
        currentUser= User.objects.get(id= request.user.id)
        currentUserProfile= UserProfile.objects.get(user__id= request.user.id)
        form= SignUpForm(request.POST or None, request.FILES or None, instance= currentUser)
        profileForm= ProfilepicForm(request.POST or None, request.FILES or None, instance= currentUserProfile)
        if form.is_valid() and profileForm.is_valid():
            form.save()
            profileForm.save()
            login(request, currentUser)
            messages.success(request, ('Your profile has been updated...'))
            return redirect('profile', username=request.user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.success(request, (f"Error: {error}"))
            for field, errors in profileForm.errors.items():
                for error in errors:
                    messages.success(request, (f"Error in {field}: {error}"))
        context={
            'form': form,
            'profileForm': profileForm,
        }
        return render(request, 'updateProfile.html', context= context)
    else:
        messages.success(request, ('You must be logged in to view this page...'))
        return redirect('index')

def logout_user(request):
    auth.logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('index')

def twit_like(request, pk):
    if request.user.is_authenticated:
        twit= get_object_or_404(Twit, id= pk)
        if twit.likes.filter(id= request.user.id):
            twit.likes.remove(request.user)
        else: 
            twit.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')
    
def twit_share(request, pk):
    # if request.user.is_authenticated:
    twit= get_object_or_404(Twit, id= pk)
    if twit:
        context={
            'twit': twit,
        }
        return render(request, 'show twit.html', context= context)
    else: 
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')
    
def twit_delete(request, pk):
    if request.user.is_authenticated:
        twit= get_object_or_404(Twit, id= pk)
        if request.user.username == twit.user.username:
            twit.delete()
            messages.success(request, ('You have successfully deleted your twit...'))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, ('Sorry, you  can\'t delete this twit because you don\'t own it ...'))
            return redirect('index')
    else:
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')
    
def twit_edit(request, pk):
    twit= get_object_or_404(Twit, id= pk)
    if request.user.is_authenticated:
        if request.user.username == twit.user.username:
            twitsForm= TwitForm(request.POST or None, instance= twit)
            if request.method == "POST":
                if twitsForm.is_valid():
                    twit= twitsForm.save(commit= False)
                    twit.user= request.user
                    twit.save()
                    messages.success(request, ('You twit has been successfully updated...'))
                    return redirect('profile', username=request.user.username)
                else:
                   for field, errors in twitsForm.errors.items():
                        for error in errors:
                            messages.success(request, (f"Error: {error}")) 
            else:
                context= {
                    'twit': twit,
                    'form': twitsForm,
                }
                return render(request, 'edit_twit.html', context= context)
        else:
            messages.success(request, ('You don\'t own this twit so you can\'t  view this page...'))
            return redirect('index')
    else:
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')
    
#unfollow
def unfollow(request, pk):
    if request.user.is_authenticated:
        profile_to_unfollow= UserProfile.objects.get(user_id= pk)
        if request.user.id == profile_to_unfollow.id:
            messages.success(request, (f'You cannot unfollow yourself...'))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            request.user.userprofile.follows.remove(profile_to_unfollow)
            request.user.userprofile.save()
            messages.success(request, (f'You have successfully unfollowed {profile_to_unfollow.user.username}...'))
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')

#follow
def follow(request, pk):
    if request.user.is_authenticated:
        profile_to_follow= UserProfile.objects.get(user_id= pk)
        request.user.userprofile.follows.add(profile_to_follow)
        request.user.userprofile.save()
        messages.success(request, (f'You have started following {profile_to_follow.user.username}...'))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')

def followers(request, username):
    if request.user.is_authenticated:
        userr = User.objects.get(username=username)
        profile= UserProfile.objects.get(user= userr)
        cuntUser= UserProfile.objects.get(user= User.objects.get(username=request.user))
        myTwits= Twit.objects.filter(user= userr)

        if request.method == "POST":
            if request.POST.get('follow'):
                cuntUser.follows.add(profile)
                messages.success(request, (f'You have started following {username}...'))
            elif request.POST.get('unfollow'):
                cuntUser.follows.remove(profile)
                messages.success(request, (f'You have successfully unfollowed {username}...'))
            cuntUser.save()
        username_followers_id= []
        for users_followers in profile.follows.all():
            username_followers_id.append(users_followers.id)
        context= {
            'user_profile': profile,
            'user_profile_ids': username_followers_id,
            'user': cuntUser.follows.all,
            'mytwits': myTwits,
        }
        return render(request, 'followers.html', context= context)
    else:
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')


def following(request, username):
    display= False
    if request.user.username == username:
        display= True
    if request.user.is_authenticated:
        userr = User.objects.get(username=username)
        profile= UserProfile.objects.get(user= userr)
        cuntUser= UserProfile.objects.get(user= User.objects.get(username=request.user))
        myTwits= Twit.objects.filter(user= userr).order_by('-twit_date')

        if request.method == "POST":
            if request.POST.get('follow'):
                cuntUser.follows.add(profile)
                messages.success(request, (f'You have started following {username}...'))
            elif request.POST.get('unfollow'):
                cuntUser.follows.remove(profile)
                messages.success(request, (f'You have successfully unfollowed {username}...'))
            cuntUser.save()
        username_followers_id= []
        for users_followers in profile.follows.all():
            username_followers_id.append(users_followers.id)
        context= {
            'display': display,
            'user_profile': profile,
            'user_profile_ids': username_followers_id,
            'user': cuntUser.follows.all,
            'mytwits': myTwits,
        }
        return render(request, 'following.html', context= context)
    else:
        messages.success(request, ('You must be logged in to perform this action...'))
        return redirect('index')

def search(request):
    if request.method == 'POST':
        user_search= request.POST['search']
        results= Twit.objects.filter(body__contains= user_search)
        context= {
            'results': results,
            }
        return render(request, 'search.html', context= context)
    else:
        context= {
                
            }
        return render(request, 'search.html', context= context) 
    
def search_user(request):
    if request.method == 'POST':
        user_search= request.POST['search']
        results= User.objects.filter(username__contains= user_search)
        context= {
            'results': results,
            }
        return render(request, 'search_user.html', context= context)
    else:
        context= {
                
            }
        return render(request, 'search_user.html', context= context) 