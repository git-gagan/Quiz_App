# Instead of creating HTML forms manually, Django has an easier way of doing it
# Here, We will be using django forms

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Defining the form and the attributes to display in the form


class MyUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {"username": "User Name", "password": "Password"}


"""
class LoggingForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput())
    class Meta:
        model = User
        fields = ["username","password"]
        labels = {"username":"User Name", "password":"Password"}"""
