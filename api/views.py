from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from my_quizzes import models
from users.utils import mail


class VerificationView(APIView):
    """
    This API view deals with the verification of newly registered users
    """
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return JsonResponse({"Status": "Registration needed"})
        if user.is_authenticated and not user.is_verified:
            otp = user.get_otp()
            mail(user.email, otp)
            return Response({"status": "Mail Sent!"})
        else:
            return JsonResponse({"status": "Verified!"})

    def post(self, request, *args, **kwargs):
        user_otp = request.data
        if self.request.user.verify_otp(user_otp):
            return Response({"status": "Successfully Verified!"})
        else:
            return Response({"status": "Verification Failed!"})


class QuizListView(generics.ListAPIView):
    """
    This view displays the List of Quizzes through API interface
    """
    queryset = models.QuizModel.objects.all()
    serializer_class = serializers.QuizSerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_verified:
            return self.list(request, *args, **kwargs)
        return JsonResponse({"Status": "Unauthorized user. ACCESS denied!"})

class QuestionListView(generics.ListAPIView):
    """
    This View deals with the display of each question of the particular Quiz
    """
    pass