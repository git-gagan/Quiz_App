from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignUp, name="Registration_Form"),
    path("Verification/", views.OTP, name="OTP Verification"),
    path("Login/", views.LogIn, name="LogIn_Form"),
    path("Home/", views.Home, name="HomeQuizzes"),
    # Angle brackets captures the part of the url to be sent to the view
    # Converter specification limits the characters matched and change the type of variable
    path("Home/<int:page_number>/", views.question_page, name="question_page")
]
