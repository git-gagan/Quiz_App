from django.contrib import admin
from .models import *

# Register your models here.
my_models = [User, QuizModel, Question, Answer]
# Looping to make it simpler and short.
for model in my_models:
    admin.site.register(model)