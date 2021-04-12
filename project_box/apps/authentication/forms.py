from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Minimum 8 characters.')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, help_text='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k: "" for k in fields}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
