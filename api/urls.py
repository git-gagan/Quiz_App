from django.urls import include, path

from . import views

urlpatterns = [
    path("users/", include('users.urls')),
    path("rest-auth/", include('rest_auth.urls')),
    path("", views.QuizListView.as_view()),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/verification/', views.VerificationView.as_view())
]