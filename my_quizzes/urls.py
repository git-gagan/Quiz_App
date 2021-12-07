from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path("", login_required(views.HomeView.as_view()), name="home-quizzes"),
    path("<int:page_number>/<name>", views.questionpage, name="question-page"),
    path("<int:page_number>/<name>/result", views.result, name="result")
]
