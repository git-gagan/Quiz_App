from django.urls import path

from . import views

urlpatterns = [
    path("", views.ApiHome.as_view(), name="api-home"),
    path("quizzes/", views.QuizListView.as_view(), name="api-quiz-list"),
    path("register/", views.RegisterView.as_view(), name="api-register"),
    path("login/", views.LoginView.as_view(), name="api-login"),
    path("logout/", views.LogoutView.as_view(), name="api-logout"),
    path('verification/', views.VerificationView.as_view(), name="api-verification"),
    path('quizzes/<uuid:quiz_id>/',
         views.QuestionListView.as_view(), name="api-question"),
    path('quizzes/<uuid:quiz_id>/result/',
         views.ResultView.as_view(), name="api-result")
]
