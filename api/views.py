from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from . import serializers
from my_quizzes import models
from users.utils import mail
from users.models import CustomUser


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
                json = {"status": "Logged In", "token": token}
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Logs the User in if verified and returns the token else sends unverified status
    """

    def post(self, request):
        user_data = self.request.data
        user_object = CustomUser.objects.filter(
            username=user_data["username"], email=user_data["email"]).first()
        if user_object:
            user_credentials = authenticate(
                request, username=user_data["username"], password=user_data["password"])
            if user_credentials:
                token = Token.objects.get_or_create(user=user_object)[0].key
                if user_object.is_verified:
                    login(self.request, user_object)
                    json = {"status": "Logged In", "token": token}
                    return Response(json)
                return Response({"status": "Can't login before OTP verification", "token": token})
        return Response("Error Logging In")


class LogoutView(APIView):
    """
    This class Logs the user out after deleting the token assigned to him
    """

    def get(self, request):
        if self.request.user.is_authenticated and self.request.user.is_verified:
            self.request.user.auth_token.delete()
            logout(self.request)
            return Response({"Status": "Succesfully Logged Out!"})
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
        token = request.META.get("HTTP_AUTHORIZATION").split()[-1]
        user = Token.objects.get(key=token).user
        if user.is_authenticated and user.is_verified:
            return self.list(request, *args, **kwargs)
        return JsonResponse({"Status": "Unauthorized user. ACCESS denied!"})


class QuestionListView(APIView):
    """
    This View deals with the display of each question of the particular Quiz
    and submits Answer by the Current User
    """

    def get_data(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").split()[-1]
        except:
            return JsonResponse({"Status": "Failing to parse token"})
        return Token.objects.get(key=token).user

    def get(self, request, *args, **kwargs):
        user = self.get_data(request)
        quiz_id = self.kwargs["quiz_id"]
        if not models.QuizModel.objects.filter(id=quiz_id):
            return JsonResponse({"Status": "The Quiz with this ID doesn't exist"})
        quiz_questions = models.Question.objects.all().filter(quiz_id=quiz_id)
        current_question_number = 1
        for question in quiz_questions:
            mcq = False
            if models.UserAnswer.objects.filter(user=user, question_id=question.id):
                current_question_number += 1
                continue
            serialized_obj = serializers.QuestionSerializer(question)
            json_obj = JSONRenderer().render(serialized_obj.data)
            if question.ques_type == question.MCQ:
                mcq = True
                answer = models.Answer.objects.filter(question=question)
                serialized_choices = serializers.AnswerSerializer(
                    answer, many=True)
                json_choices = JSONRenderer().render(serialized_choices.data)
            if mcq:
                return Response({"Question": json_obj, "Options": json_choices})
            return Response({"Question": json_obj})
        return Response({"Status": "Quiz Completed!"})

    def post(self, request, *args, **kwargs):
        user = self.get_data(request)
        if models.UserAnswer.objects.filter(user=user, question_id=request.data["question"]):
            return Response({"Status": "Already Attempted"})
        serializer = serializers.UserAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"Status": "Success"})
        return Response({"Status": "Failure", "error": serializer.errors})


class ResultView(APIView):
    """
    This view deals with the Quiz Result and score for each quiz
    """

    def get(self, request, *args, **kwargs):
        if self.kwargs['quiz_id'] > len(models.QuizModel.objects.all()):
            return Response({"Status": "The Quiz with this ID doesn't exist!!"})
        try:
            token = request.META.get("HTTP_AUTHORIZATION").split()[-1]
        except:
            return JsonResponse({"Status": "Failing to parse token"})
        user = Token.objects.get(key=token).user
        quiz_id = self.kwargs['quiz_id']
        quiz_questions = models.Question.objects.all().filter(quiz_id=quiz_id)
        user_answers = models.UserAnswer.objects.all().filter(
            user_id=user, question__quiz=quiz_id)
        answers = models.Answer.objects.all().filter(
            question__quiz=quiz_id, is_correct=True)
        if len(user_answers) < len(quiz_questions):
            return Response({"Status": "Please attempt the whole quiz to see the results"})
        total_score = 0
        user_score = 0
        for question in quiz_questions:
            total_score += question.ques_score
        for i in range(len(user_answers)):
            if user_answers[i].question.ques_type == "FIB":
                if user_answers[i].text.lower() == models.Answer.objects.filter(question_id=user_answers[i].question).first().solutions.lower():
                    user_score += models.Question.objects.filter(
                        id=user_answers[i].question.id).first().ques_score
            elif user_answers[i].choice.is_correct:
                user_score += answers[i].question.ques_score
        quiz_name = models.QuizModel.objects.filter(id=quiz_id).first()
        return Response({
            "Message": "Thanks for attempting the Quiz",
            "Quiz Name": quiz_name.quiz_name,
            "Your Score": user_score,
            "Total Score": total_score
        })
