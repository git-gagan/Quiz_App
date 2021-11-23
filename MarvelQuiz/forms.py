# Instead of creating HTML forms manually, Django has an easier way of doing it
# Here, We will be using django forms

from django import forms
from django.forms.widgets import PasswordInput
from .models import User

# Defining the form and the attributes to display in the form

class MyUserForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput())
    class Meta:
        model = User
        fields = ["user_name", "ph_num", "password", "email"]
        labels = {"user_name":"User Name", "ph_num":"Phone Number", "password":"Password",\
            "email":"Email ID"}