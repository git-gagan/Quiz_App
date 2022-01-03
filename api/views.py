from datetime import datetime

from django.contrib.auth import authenticate, logout
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from .utils import get_user
from my_quizzes import models
from users.utils import mail
from users.models import CustomUser


class ApiHome(APIView):
    """
    API Home view with a Welcome and status response
    """

    def get(self, request, *args, **kwargs):
        return Response({
            "Message": "Welcome to Quizzer App REST Implementation",
            "Status": "Please register/login and Verify to proceed."
        })


class RegisterView(APIView):
    """
    Creates the User after validating all the credentials and generates the token
    """

    def post(self, request):
        print(request.data)
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get_or_create(user=user)[0].key
                json = {"status": "Registered", "token": token}
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Logs the User in if verified and returns the token else sends unverified status
    """

    def post(self, request):
        user_data = self.request.data
        if "username" not in user_data or "email" not in user_data or "password" not in user_data:
            return Response({
                "Status": "Please check if you have provided username, email, password"
            })
        user_object = CustomUser.objects.filter(
            username=user_data["username"], email=user_data["email"]).first()
        if user_object:
            user_credentials = authenticate(
                self.request, username=user_data["username"], password=user_data["password"])
            if user_credentials:
                token = Token.objects.get_or_create(user=user_object)[0].key
                if user_object.is_verified:
                    json = {"status": "Logged In", "token": token}
                    return Response(json)
                return Response({"status": "Can't login before OTP verification", "token": token})
        return Response({"status":"Error Logging In"})


class LogoutView(APIView):
    """
    This class Logs the user out after deleting the token assigned to him
    """

    def get(self, request):
        user = get_user(request)
        if not user:
            return Response({"Status": "Cannot Authorize"})
        if user.is_authenticated and user.is_verified:
            user.auth_token.delete()
            logout(self.request)
            return Response({"Status": "Succesfully Logged Out!"})
        return Response({"Status": "Login First"})


class VerificationView(APIView):
    """
    This API view deals with the verification of newly registered users
    """

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if not user:
            return Response({"status": "Cannot Authorize"})
        if user.is_authenticated and not user.is_verified:
            otp = user.get_otp()
            mail(user.email, otp)
            return Response({"status": "Mail Sent"})
        else:
            return Response({"status": "Verified"})

    def post(self, request, *args, **kwargs):
        user = get_user(request)
        if user == None or "otp" not in request.data:
            return JsonResponse({"status": "Invalid POST request!"})
        user_otp = request.data["otp"]
        if user.verify_otp(user_otp):
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
        user = get_user(request)
        if not user:
            return Response({"status": "Cannot Authorize"})
        if user.is_authenticated and user.is_verified:
            return self.list(request, *args, **kwargs)
        return JsonResponse({"status": "Unverified user. ACCESS denied!"})


class QuestionListView(APIView):
    """
    This View deals with the display of each question of the particular Quiz
    and submits Answer by the Current User
    """

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if not user:
            return Response({"Status": "Cannot Authorize"})
        if not user.is_verified:
            return JsonResponse({"Status": "Unauthorized user. ACCESS denied!"})
        quiz_id = self.kwargs["quiz_id"]
        if not models.QuizModel.objects.filter(id=quiz_id):
            return JsonResponse({"Status": "The Quiz with this ID doesn't exist"})
        this_quiz = models.QuizModel.objects.all().filter(id=quiz_id).first()
        quiz_questions = models.Question.objects.all().filter(quiz_id=quiz_id)
        current_question_number = 1
        for question in quiz_questions:
            mcq = False
            if models.UserAnswer.objects.filter(user=user, question_id=question.id):
                current_question_number += 1
                continue
            if current_question_number == 1 and not models.QuizTaken.objects.filter(user=user, quiz=this_quiz):
                quiz_taken = models.QuizTaken.objects.create(
                    user=user, quiz=this_quiz, start_time=datetime.now())
                quiz_taken.save()
            quiz_taken = models.QuizTaken.objects.filter(
                user=user, quiz=this_quiz).first()
            time_used = (
                datetime.now()-quiz_taken.start_time.replace(tzinfo=None)).total_seconds()
            time_remaining = round((this_quiz.timer) - time_used)
            if time_used >= this_quiz.timer:
                return Response({"Status": "Time's UP!"})
            serialized_obj = serializers.QuestionSerializer(question)
            if question.ques_type == question.MCQ:
                mcq = True
                answer = models.Answer.objects.filter(question=question)
                serialized_choices = serializers.AnswerSerializer(
                    answer, many=True)
            if mcq:
                return Response({"Question": serialized_obj.data, "Options": serialized_choices.data, "Time-Left": time_remaining})
            return Response({"Question": serialized_obj.data, "Time-Left": time_remaining})
        return Response({"Status": "Quiz Completed!"})

    def post(self, request, *args, **kwargs):
        user = get_user(request)
        if not user:
            return JsonResponse({"Status": "Cannot Authorize"})
        if not user.is_verified:
            return JsonResponse({"Status": "Unauthorized user. ACCESS denied!"})
        quiz_taken = models.QuizTaken.objects.filter(
            user=user, quiz=self.kwargs["quiz_id"]).first()
        if not quiz_taken:
            return Response({"Status": "Please Attempt the Quiz First!"})
        if (datetime.now()-quiz_taken.start_time.replace(tzinfo=None)).total_seconds() > quiz_taken.quiz.timer:
            return Response({"Status": "Time's UP!"})
        serializer = serializers.UserAnswerSerializer(data=request.data)
        if serializer.is_valid():
            if "choice" not in request.data and "text" not in request.data:
                return Response({
                    "Status": "Please provide one of choice or text depending upon question type"
                })
            if models.UserAnswer.objects.filter(user=user, question_id=request.data["question"]):
                return Response({"Status": "Already Attempted"})
            serializer.save(user=user)
            return Response({"Status": "Success"})
        return Response({"Status": "Failure", "error": serializer.errors})


class ResultView(APIView):
    """
    This view deals with the Quiz Result and score for each quiz
    """

    def get(self, request, *args, **kwargs):
        if not models.QuizModel.objects.all().filter(id=self.kwargs['quiz_id']):
            return Response({"Status": "The Quiz with this ID doesn't exist!!"})
        user = get_user(request)
        if not user:
            return JsonResponse({"Status": "Cannot Authorize"})
        if not user.is_verified:
            return JsonResponse({"Status": "Unauthorized user. ACCESS denied!"})
        quiz_id = self.kwargs['quiz_id']
        quiz_questions = models.Question.objects.all().filter(quiz_id=quiz_id)
        user_answers = models.UserAnswer.objects.all().filter(
            user_id=user, question__quiz=quiz_id)
        answers = models.Answer.objects.all().filter(
            question__quiz=quiz_id, is_correct=True)
        quiz_taken = models.QuizTaken.objects.filter(
            user=user, quiz_id=self.kwargs['quiz_id']).first()
        if not quiz_taken:
            return Response({"Status": "Please attempt the quiz to see results"})
        time_difference = (
            datetime.now() - quiz_taken.start_time.replace(tzinfo=None)).total_seconds()
        if time_difference < quiz_taken.quiz.timer and len(user_answers) < len(quiz_questions):
            return Response({"Status": "Please attempt the whole quiz to see the results"})
        total_score = 0
        user_score = 0
        for question in quiz_questions:
            total_score += question.ques_score
            user_answer = models.UserAnswer.objects.filter(
                user=user, question=question).first()
            if not user_answer:
                user_answer = models.UserAnswer.objects.create(
                    user=user, question=question)
                if question.ques_type == question.FIB:
                    user_answer.text = ""
                else:
                    user_answer.choice = None
                user_answer.save()
            else:
                if question.ques_type == question.FIB:
                    if user_answer.text == models.Answer.objects.filter(question=user_answer.question).first().solutions.lower():
                        user_score += models.Question.objects.filter(
                            id=user_answer.question.id).first().ques_score
                else:
                    if user_answer.choice and user_answer.choice.is_correct:
                        user_score += user_answer.question.ques_score
        user_answers = models.UserAnswer.objects.all().filter(
            user_id=user, question__quiz=quiz_id)
        serialized_quiz_questions = serializers.QuestionSerializer(
            quiz_questions, many=True)
        serialized_user_answers = serializers.UserAnswerSerializer(
            user_answers, many=True)
        serialized_answers = serializers.AnswerSerializer(answers, many=True)
        return Response({
            "Message": "Thanks for attempting the Quiz",
            "Quiz Name": quiz_taken.quiz.quiz_name,
            "Questions": serialized_quiz_questions.data,
            "Answers": serialized_answers.data,
            "Your Answers": serialized_user_answers.data,
            "Your Score": user_score,
            "Total Score": total_score,
        })
