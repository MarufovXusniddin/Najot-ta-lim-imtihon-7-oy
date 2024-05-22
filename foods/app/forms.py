from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Comment, ShippingAddress


class RegisterForm(UserCreationForm):
    firstname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    lastname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(max_length=55, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(max_length=28, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(max_length=28, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(max_length=28, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Text'
            })
        }


class BookForm(forms.ModelForm):
    firstname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ism'
    }))
    lastname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Familiya'
    }))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    mobile = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone number'
    }))

    class Meta:
        model = ShippingAddress
        fields = ['firstname', 'lastname', 'email', 'mobile']