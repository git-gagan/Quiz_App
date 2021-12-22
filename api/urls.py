from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.QuizListView.as_view(), name="api-quiz-list"),
    path("register/", views.RegisterView.as_view(), name="api-register"),
    path("login/", views.LoginView.as_view(), name="api-login"),
    path("logout/", views.LogoutView.as_view(), name="api-logout"),
    path('verification/', views.VerificationView.as_view(), name="api-verification"),
    path('<int:quiz_id>/', views.QuestionListView.as_view(), name="api-question")
]
