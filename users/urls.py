from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("verification/", views.verification, name="verification"),
    path("login/", views.LoginUser.as_view(), name="login"),
]
