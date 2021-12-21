from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from my_quizzes import models
        

class CustomRegisterSerializer(RegisterSerializer):
    pass


class QuizSerializer(serializers.ModelSerializer):
    "Class dealing with serialization of QuizModel fields"
    class Meta:
        model = models.QuizModel
        fields = ('quiz_name', 'timer')
        
