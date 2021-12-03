from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home-quizzes")
]

"""path("Login/", views.logging, name="LogIn_Form"),
path("Home/<page_number>/", views.question_page, name="question_page")"""