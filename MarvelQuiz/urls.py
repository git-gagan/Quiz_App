from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignUp, name="Registration_Form"),
    path("Verification/", views.OTP, name="OTP Verification"),
    path("Login/", views.LogIn, name="LogIn_Form")
]
