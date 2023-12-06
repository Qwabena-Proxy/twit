from django import forms
from .models import *

class TwitForm(forms.ModelForm):
    body= forms.CharField(
        required= True, 
        widget= forms.widgets.Textarea(
            attrs={
                'rows': '15',
                'cols': '80',
                'placeholder': "Enter your twits here..",
                'class': 'border-0 px-3 py-3 bg-gray-300 placeholder-black text-gray-800 rounded text-sm shadow focus:outline-none w-full'
            }
        ), 
        label='',

    )

    class Meta:
        model= Twit
        exclude= ('user',)