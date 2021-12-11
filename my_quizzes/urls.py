from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", login_required(views.HomeView.as_view()), name="home-quizzes"),
    path("<int:page_number>/",
         login_required(views.QuestionPageView.as_view()), name="question-page"),
    path("<int:page_number>/result/",
         login_required(views.ResultView.as_view()), name="result")
]
