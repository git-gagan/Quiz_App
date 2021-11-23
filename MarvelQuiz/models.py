from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Creating Models for my MarvelQuiz App
# A model is a single source of truth about the Data we are storing

class User(models.Model):
    """
    This is the User model which consists of User Specific Data 
    primarily intended to be user for Registration and Login purposes
    """
    user_name = models.CharField("User Name", max_length=30, unique = True)
    ph_num = PhoneNumberField("Phone Number", unique = True)
    password = models.CharField("Password", max_length=20)
    email = models.EmailField("Email ID", unique = True)
    