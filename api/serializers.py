from rest_framework import serializers
from my_quizzes import models
from users.models import CustomUser
        

class UserSerializer(serializers.ModelSerializer):
    """
    API representation of CustomUser Model
    """
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user


class QuizSerializer(serializers.ModelSerializer):
    "Class dealing with serialization of QuizModel fields"
    class Meta:
        model = models.QuizModel
        fields = ('quiz_name', 'timer')
        

class QuestionSerializer(serializers.ModelSerializer):
    "Class dealing with serialization of Questions one at a time"
    class Meta:
        model = models.Question
        fields = ('ques_text',)