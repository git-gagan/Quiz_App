from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("register/", views.Register.as_view(), name="register"),
    path("verification/", views.Verification.as_view(), name="verification"),
    path("login/", views.LoginUser.as_view(), name="login"),
]
