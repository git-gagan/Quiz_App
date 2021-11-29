from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Creating Models for my MarvelQuiz App
# A model is a single source of truth about the Data we are storing

class User(models.Model):
    """
    This is the User model which consists of User Specific Data 
    primarily intended to be user for Registration and Login purposes
    """
    user_name = models.CharField("User Name", max_length=30, unique = True)
    ph_num = PhoneNumberField("Phone Number", unique = True)
    password = models.CharField("Password", max_length=20)
    email = models.EmailField("Email ID", unique = True)
    is_verified = models.BooleanField("Authentication Status", default=False)
    def __str__(self):
        return self.user_name
    
class QuizModel(models.Model):
    """
    This class deals with the Quiz data for each particular quiz.
    The Idea is to have 2 quizzes only in the beginning (Technical/Fantasy Movie)
    NOTE:- We will use Auto incremented Django Field ID as primary key, so need not to add.
    """
    Quiz_Name = models.CharField(unique = True, max_length = 20)
    timer = models.IntegerField("Timer")
    def __str__(self):
        return self.Quiz_Name

class Question(models.Model):
    """
    This class has data fields representing each particular question
    The question can be both MCQ or FIB which is determined by the type field
    Also, quiz_id is the foreign key which maps to QuizModel.
    """
    ques_text = models.CharField("Question", max_length=40)
    ques_score = models.SmallIntegerField("Marks")
    ques_type = models.CharField("Type", max_length=3)
    quiz_id = models.ForeignKey(QuizModel, on_delete=models.CASCADE) 
    def __str__(self):
        return self.ques_text

class Answer(models.Model):
    """
    This model deals with the answers of all the questions
    It includes all the choices for MCQ with additional parameter to specify the right one
    """
    ques_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    solutions = models.CharField("Solution", max_length=50)
    is_correct = models.BooleanField("Correct", null=True)
    
    