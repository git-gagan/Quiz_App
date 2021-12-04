from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home-quizzes"),
    path("<int:page_number>/<name>", views.questionpage, name="question-page")
]

