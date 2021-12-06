from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import HttpResponse, request
from .models import Answer, Question, QuizModel, UserAnswer
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
    this_quiz = QuizModel.objects.all().filter(id=page_number).first()
    quiz_questions = Question.objects.all().filter(quiz_id=page_number)
    for question in quiz_questions:
        if UserAnswer.objects.all().filter(user_id=request.user, question_id=question.id):
            pass
        else:
            if request.method == "POST":
                answer = UserAnswer(user=request.user, question_id=question.id)
                if question.ques_type == "FIB":
                    user_answer = request.POST.get("answer").lower()
                    answer.text = user_answer
                else:
                    user_choice = request.POST.get("choice")
                    user_object = Answer.objects.all().filter(
                        question_id=question.id, solutions=user_choice).first()
                    answer.choice = user_object
                answer.save()
                return redirect(f"/home/{page_number}/{name}")
            answers = Answer.objects.all().filter(question_id=question.id)
            return render(request, "onequestion.html", {
                "this_quiz": this_quiz, "question": question, "answers": answers
            })
    else:
        return redirect(f"/home/{page_number}/{name}/result")


@login_required
def result(request, page_number, name):
    quiz_questions = Question.objects.all().filter(quiz_id=page_number)
    user_answers = UserAnswer.objects.all().filter(
        user_id=request.user, question__quiz=page_number)
    answers = Answer.objects.all().filter(question__quiz=page_number)
    total_score = 0
    user_score = 0
    for question in quiz_questions:
        total_score += question.ques_score
    for i in range(len(user_answers)):
        if user_answers[i].question.ques_type == "FIB":
            if user_answers[i].text != answers[i].solutions.lower():
                continue
        else:
            if not user_answers[i].choice.is_correct:
                continue
        user_score += answers[i].question.ques_score

    context = {
        "quiz_number": page_number,
        "quiz_name": name,
        "questions": quiz_questions,
        "user_answers": user_answers,
        "answers": answers,
        "total_score": total_score,
        "user_score": user_score
    }
    return render(request, "resultpage.html", context)
