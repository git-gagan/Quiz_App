from django.shortcuts import render
from rest_framework import generics

from . import serializers
from users import models

class UserListView(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

