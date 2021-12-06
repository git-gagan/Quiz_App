from django.db import models
from users.models import CustomUser

# A model is a single source of truth about the Data we are storing


class QuizModel(models.Model):
    """
    This class deals with the Quiz data for each particular quiz.
    The Idea is to have 2 quizzes only in the beginning (Technical/Fantasy Movie)
    NOTE:- We will use Auto incremented Django Field ID as primary key, so need not to add.
    """
    quiz_name = models.CharField(unique=True, max_length=20)
    timer = models.IntegerField("Timer")

    def __str__(self):
        return self.quiz_name


class Question(models.Model):
    """
    This class has data fields representing each particular question
    The question can be both MCQ or FIB which is determined by the type field
    Also, quiz_id is the foreign key which maps to QuizModel.
    """
    ques_text = models.CharField("Question", max_length=40)
    ques_score = models.SmallIntegerField("Marks")
    ques_type = models.CharField("Type", max_length=3)
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.ques_text


class Answer(models.Model):
    """
    This model deals with the answers of all the questions
    It includes all the choices for MCQ with additional parameter to specify the right one
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    solutions = models.CharField("Solution", max_length=50)
    is_correct = models.BooleanField("Correct", null=True)


class UserAnswer(models.Model):
    """
    This model deals with the answers submitted by the user
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField("User's Answer", max_length=30, null=True, blank=True)
    choice = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
