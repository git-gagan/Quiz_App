from django.urls import path

from .views import *

urlpatterns =[
    path("", ApiHomeView.as_view(), name="api-home-view"),
]