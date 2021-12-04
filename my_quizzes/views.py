from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, request
from .models import Answer, Question, QuizModel
from django.shortcuts import redirect, render


@login_required
def home(request):
    all_quizzes = QuizModel.objects.all()
    return render(request, "homepage.html", {"quizzes": all_quizzes})


@login_required
def questionpage(request, page_number, name):
    """
    This view renders the template for display of each particular quiz.
    """
    if page_number > len(QuizModel.objects.all()):
        return HttpResponse("The Quiz with this ID doesn't exist!!")
    this_quiz = QuizModel.objects.all().filter(id = page_number).first()
    quiz_questions = Question.objects.all().filter(quiz = page_number)
    #answers = Answer.objects.all().filter(question = this_question.id)
    return render(request, "onequestion.html", {
        "this_quiz":this_quiz, "question":quiz_questions, "answers":""
        })
    
def result(request):
    pass
        

