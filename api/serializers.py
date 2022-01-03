from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers
from my_quizzes import models
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    API representation of CustomUser Model
    """
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def create(self, validated_data):
        password2 = validated_data.pop("password2")
        user = CustomUser(**validated_data)
        try:
            password_validation.validate_password(
                validated_data["password"], user=user)
        except ValidationError as error:
            raise serializers.ValidationError(str(error))
        if validated_data["password"] != password2:
            raise serializers.ValidationError({"Error": "Password Mismatch"})
        user.set_password(validated_data['password'])
        user.save()
        return user


class QuizSerializer(serializers.ModelSerializer):
    "Class dealing with serialization of QuizModel fields"
    class Meta:
        model = models.QuizModel
        fields = ('id', 'quiz_name', 'timer')


class QuestionSerializer(serializers.ModelSerializer):
    "Class dealing with serialization of Questions one at a time"
    class Meta:
        model = models.Question
        fields = ('id', 'ques_text', 'ques_type',)


class AnswerSerializer(serializers.ModelSerializer):
    """
    Actual Answer serializer
    """
    class Meta:
        model = models.Answer
        fields = ('id', 'solutions',)


class UserAnswerSerializer(serializers.ModelSerializer):
    """
    Class for serializing answer of users and saving them as well when the serializer is called
    """
    class Meta:
        model = models.UserAnswer
        fields = ('question', 'text', 'choice',)

    def create(self, validated_data):
        user_answer = models.UserAnswer.objects.create(**validated_data)
        return user_answer
