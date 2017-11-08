from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import *

class SignupForm( UserCreationForm ):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': '아이디',
                                   }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '패스워드',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '패스워드 확인',
    }))
    phoneNumber = forms.CharField(max_length=13, required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': '전화번호 [ - 없이, ex) 010xxxxxxxx ]',
                                  }))
    name = forms.CharField(max_length=20,required=False,
                           widget=forms.TextInput(
                               attrs={
                                   'class':'form-control',
                                   'placeholder':'이름',
                               }))
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder':'이메일',
                                }))

    class Meta:
        model = User
        fields = ('username','name','password1','password2','phoneNumber','email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name','phoneNumber','zipCode','streetName','detailAddress','subAddress','email')

