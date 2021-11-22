from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignUp, name="Registration Form"),
    path("HomePage/", views.HomePage, name="Registration Form"),
]
