# Instead of creating HTML forms manually, Django has an easier way of doing it
# Here, We will be using django forms

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

# Defining the form and the attributes to display in the form

# Workaround to make email mandatory without creating CustomUser
CustomUser._meta.get_field('email')._unique = True


class MyUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
        labels = {"username": "User Name", "password": "Password"}
