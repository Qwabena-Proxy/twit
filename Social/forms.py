from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


#Profilepic form
class ProfilepicForm(forms.ModelForm):
    Profileimage= forms.ImageField(
        label='Profile Image',
        required= False,
        widget= forms.widgets.FileInput(
            attrs={
                'class': 'bg-gray-900 text-white text-center mx-auto hover:bg-gray-800 text-sm font-bold lowercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1',
                'type': 'file',
              'style': 'transition: all 0.15s ease 0s;',
            }
        )
    )
    bio = forms.CharField(
        label='Profile bio',
        required= False,
        widget=forms.Textarea(
            attrs={
                'rows': '15',
                'cols': '80',
                'placeholder': "Enter your profile bio here..",
                'class': 'border-0 px-3 py-3 bg-gray-300 placeholder-gray-700 text-gray-800 rounded text-sm shadow focus:outline-none w-full mb-2'
            }
        )
    )
    homepage_link = forms.CharField(
        label='Website link',
        required= False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Website link',
                'class': 'border-0 px-3 py-3 rounded mb-3 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400',
                'style': 'transition: all 0.15s ease 0s;',
            }
        )
    )
    github_link = forms.CharField(
        label='Github link',
        required= False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Github link',
                'class': 'border-0 px-3 py-3 rounded mb-3 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400',
                'style': 'transition: all 0.15s ease 0s;',
            }
        )
    )
    twitter_link = forms.CharField(
        label='Twitter link',
        required= False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Twitter link',
                'class': 'border-0 px-3 py-3 rounded mb-3 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400',
                'style': 'transition: all 0.15s ease 0s;',
            }
        )
    )

    class Meta:
        model= UserProfile
        fields= ('Profileimage', 'bio', 'homepage_link', 'github_link', 'twitter_link')

class TwitForm(forms.ModelForm):
    body= forms.CharField(
        required= True, 
        widget= forms.widgets.Textarea(
            attrs={
                'rows': '15',
                'cols': '80',
                'placeholder': "Enter your twits here..",
                'class': 'border-0 px-3 py-3 bg-gray-300 placeholder-gray-700 text-gray-800 rounded text-sm shadow focus:outline-none w-full'
            }
        ), 
        label='',

    )

    class Meta:
        model= Twit
        exclude= ('user', 'likes', )

class SignUpForm(UserCreationForm):
    email= forms.EmailField(
        label='E-mail',
        required= True,
        widget= forms.widgets.EmailInput(
            attrs={
                'placeholder': 'E-mail',
                'class': 'border-0 px-3 py-3 rounded mb-3 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400',
                'style': 'transition: all 0.15s ease 0s;',
            }
        )
    )

    first_name= forms.CharField(
        max_length=100,
        label='First Name',
        required= False,
        widget= forms.widgets.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'border-0 px-3 py-3 rounded mb-3 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400',
                'style': 'transition: all 0.15s ease 0s;',
            }
        )
    )

    last_name= forms.CharField(
        max_length=100,
        label='Last Name',
        required= False,
        widget= forms.widgets.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'border-0 px-3 py-3 rounded mb-3 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400',
                'style': 'transition: all 0.15s ease 0s;',
            }
        )
    )

    class Meta:
        model= User
        fields= ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Creating username field
        self.fields['username'].widget.attrs['placeholder']= 'Username'
        self.fields['username'].widget.attrs['class']= 'border-0 px-3 py-3 rounded mb-2 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400'
        self.fields['username'].widget.attrs['style']= 'transition: all 0.15s ease 0s;'
        self.fields['username'].label= 'Username'
        self.fields['username'].required= True
        self.fields['username'].help_text= None

        # Creating password1 field
        self.fields['password1'].widget.attrs['placeholder']= 'Password'
        self.fields['password1'].widget.attrs['class']= 'border-0 px-3 py-3 rounded mb-2 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400'
        self.fields['password1'].widget.attrs['style']= 'transition: all 0.15s ease 0s;'
        self.fields['password1'].widget.label= 'Password'
        self.fields['password1'].widget.required= True
        self.fields['password1'].help_text= None

        # Creating password2 field
        self.fields['password2'].widget.attrs['placeholder']= 'Confirm password'
        self.fields['password2'].widget.attrs['class']= 'border-0 px-3 py-3 rounded mb-2 text-sm shadow w-full bg-gray-300 placeholder-gray-700 text-gray-800 outline-none focus:bg-gray-400'
        self.fields['password2'].widget.attrs['style']= 'transition: all 0.15s ease 0s;'
        self.fields['password2'].widget.label= 'Confirm Password'
        self.fields['password2'].widget.required= True
        # self.fields['password1'].help_text= None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and username != self.initial.get('username'):
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('This username is already taken. Please choose a different username.')
        return username