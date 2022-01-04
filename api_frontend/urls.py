from django.urls import path

from .views import *

urlpatterns =[
    path("", ApiHomeView.as_view(), name="api-home-view"),
    path("api-login/", ApiLoginView.as_view(), name="api-loginuser"),
    path("api-registration/", ApiRegistrationView.as_view(), name="api-registration"),
    path("api-verification/", ApiVerificationView.as_view(), name="api-verification"),
    path("quiz/", ApiQuizzesView.as_view(), name="quizzes"),
    path("quiz/<uuid:quiz_id>/", ApiQuestionsView.as_view(), name="api-question")
]