from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup, name="Registration_Form"),
    path("Verification/", views.otp, name="OTP Verification"),
    path("Login/", views.login, name="LogIn_Form"),
    path("Home/", views.home, name="HomeQuizzes"),
    # Angle brackets captures the part of the url to be sent to the view
    # Converter specification limits the characters matched and change the type of variable
    path("Home/<page_number>/", views.question_page, name="question_page")
]
