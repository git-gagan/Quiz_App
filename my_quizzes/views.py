from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, request
from .models import Answer, Question, QuizModel
from django.shortcuts import redirect, render

# Views here

"""def logging(request):
    This view deals with the login functionality verifying the credentials of the user.
    if request.method == "POST":
        form = LoggingForm(request.POST)
        this_user = request.POST.get("username")
        this_user_pass = request.POST.get("password")
        print(this_user,this_user_pass)
        user = authenticate(request, username=this_user, password=this_user_pass)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect("/Home/")
        else:
            return HttpResponse("Invalid Credentials")
    else:
        form = LoggingForm()
    return render(request, "LogInform.html", {"form":form}) 
"""
# @login_required


def home(request):
    #request.session["question_number"] = 0
    all_quizzes = QuizModel.objects.all()
    return render(request, "HomePage.html", {"quizzes": all_quizzes})


"""

#This decorator works with inbuilt authentication system
#@login_required
def question_page(request, page_number):
    This view renders the template for display of each particular quiz.
    for i in range(len(page_number)):
        if page_number[i].isdigit():
            break
    quiz_number = int(page_number[i:])
    if quiz_number > len(QuizModel.objects.all()):
        return HttpResponse("The Quiz with this ID doesn't exist!!")
    this_quiz = QuizModel.objects.all().filter(id = quiz_number).first()
    quiz_questions = Question.objects.all().filter(quiz = quiz_number)
    print("----------------",request.session["question_number"],"----------------")
    #Logical Error when user presses the back button
    if request.method == "POST":
        request.session["question_number"] += 1
        if request.session["question_number"] > len(quiz_questions)-1:
            return render(request, "result.html")
        return HttpResponseRedirect(f"/Home/quiz{this_quiz.id}")
    this_question = quiz_questions[request.session["question_number"]]
    answers = Answer.objects.all().filter(question = this_question.id)
    return render(request, "onequestion.html", {
        "this_quiz":this_quiz, "question":this_question, "answers":answers
        })
"""
