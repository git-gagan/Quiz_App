from django.contrib.auth import login, logout
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from users.models import CustomUser

from . import serializers
from my_quizzes import models
from users.utils import mail


class RegisterView(APIView):
    """
    Creates the User
    """
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get_or_create(user=user)[0].key
                json = {"status":"Logged In", "token":token}
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    Logs the User in if verified and returns the token else sends unverified status
    """

    def post(self, request):
        user_data = self.request.data
        user_object = CustomUser.objects.filter(username=user_data["username"]).first()
        if user_object:
            token = Token.objects.get_or_create(user=user_object)[0].key
            if user_object.is_verified:
                login(self.request, user_object)
                json = {"status":"Logged In", "token":token}
                return Response(json)
            return Response({"status":"Can't login before OTP verification", "token":token})
        return Response("Error Logging In")

class LogoutView(APIView):
    """
    This class Logs the user out after deleting the token assigned to him
    """

    def get(self, request):
        if self.request.user.is_authenticated and self.request.user.is_verified:
            self.request.user.auth_token.delete()
            logout(self.request)
            return Response({"Status":"Succesfully Logged Out!"})
        return Response({"Status": "Login First"})

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
        user_otp = request.data["otp"]
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


class QuestionListView(APIView):
    """
    This View deals with the display of each question of the particular Quiz
    """

    def get(self, request, *args, **kwargs):
        quiz_id = self.kwargs["quiz_id"]
        quiz_questions = models.Question.objects.all().filter(quiz_id=quiz_id).first()
        serialized_obj = serializers.QuestionSerializer(quiz_questions)
        json_obj = JSONRenderer().render(serialized_obj.data)
        return Response({"Question": json_obj})
