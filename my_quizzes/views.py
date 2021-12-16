from datetime import datetime

from django.views import generic
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .models import Answer, Question, QuizModel, UserAnswer, QuizTaken


@method_decorator(never_cache, name='dispatch')
class HomeView(generic.ListView):
    """
    This generic view renders all the quizzes on the homepage.
    Login required is enabled for it in URL configuration.
    """
    template_name = "homepage.html"
    context_object_name = "quizzes"

    def get_queryset(self):
        self.request.session["timeup"] = False
        return QuizModel.objects.all()


@method_decorator(never_cache, name='dispatch')
class QuestionPageView(TemplateView):
    """
    This view deals with rendering of questions one by one and
    Saving them in the answer model
    """
    template_name = "onequestion.html"

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        if self.kwargs['page_number'] > len(QuizModel.objects.all()):
            return HttpResponse("The Quiz with this ID doesn't exist!!")
        return handler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.kwargs["page_number"]
        context["page_number"] = page_number
        this_quiz = QuizModel.objects.all().filter(id=page_number).first()
        quiz_questions = Question.objects.all().filter(quiz_id=page_number)
        current_question_number = 1
        for question in quiz_questions:
            if UserAnswer.objects.all().filter(user_id=self.request.user, question_id=question.id):
                current_question_number += 1
                continue
            if current_question_number == 1 and not QuizTaken.objects.filter(user=self.request.user, quiz=this_quiz):
                quiz_taken = QuizTaken.objects.create(
                    user=self.request.user, quiz=this_quiz, start_time=datetime.now())
                quiz_taken.save()
            quiz_taken = QuizTaken.objects.filter(
                user=self.request.user, quiz=this_quiz).first()
            time_used = (
                datetime.now()-quiz_taken.start_time.replace(tzinfo=None)).total_seconds()
            time_remaining = round((this_quiz.timer) - time_used)
            if time_used >= this_quiz.timer:
                messages.warning(self.request, "Time's UP!")
                context["timeup"] = True
                self.request.session["timeup"] = True
            answers = Answer.objects.all().filter(question_id=question.id)
            context["remaining_time"] = time_remaining
            context["this_quiz"] = this_quiz
            context["question"] = question
            context["answers"] = answers
            context["question_number"] = current_question_number
            context["total_questions"] = quiz_questions.count()
            return context
        else:
            context["Completed"] = True
        return context

    def post(self, request, **kwargs):
        id = self.request.POST.get("question")
        question = Question.objects.filter(id=id).first()
        answer = UserAnswer(user=self.request.user, question_id=id)
        if question.ques_type == "FIB":
            user_answer = self.request.POST.get("answer").lower()
            answer.text = user_answer
        else:
            user_choice = self.request.POST.get("choice")
            user_object = Answer.objects.all().filter(
                question_id=id, solutions=user_choice).first()
            answer.choice = user_object
        answer.save()
        return redirect(f"/quizzes/{self.kwargs['page_number']}/")


@method_decorator(never_cache, name='dispatch')
class ResultView(TemplateView):
    """
    This view renders the result page with appropriate values and data
    """
    template_name = "resultpage.html"

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        if self.kwargs['page_number'] > len(QuizModel.objects.all()):
            return HttpResponse("The Quiz with this ID doesn't exist!!")
        return handler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["incomplete"] = False
        page_number = self.kwargs['page_number']
        quiz_questions = Question.objects.all().filter(quiz_id=page_number)
        user_answers = UserAnswer.objects.all().filter(
            user_id=self.request.user, question__quiz=page_number)
        answers = Answer.objects.all().filter(
            question__quiz=page_number, is_correct=True)
        if len(user_answers) < len(quiz_questions) and not self.request.session["timeup"]:
            messages.warning(
                self.request, "Please attempt the whole quiz to continue")
            context["incomplete"] = True
            return context
        total_score = 0
        user_score = 0
        for question in quiz_questions:
            total_score += question.ques_score
            user_answer = UserAnswer.objects.filter(user=self.request.user, question=question).first()
            if not user_answer:
                user_answer = UserAnswer.objects.create(user=self.request.user, question=question)
                if question.ques_type == question.FIB:
                    user_answer.text = ""
                else:
                    user_answer.choice = None
                user_answer.save()
            else:
                if question.ques_type == question.FIB:
                    if user_answer.text == Answer.objects.filter(question=user_answer.question).first().solutions.lower():
                        user_score += Question.objects.filter(
                            id=user_answer.question.id).first().ques_score
                else:
                    if user_answer.choice and user_answer.choice.is_correct:
                        user_score += user_answer.question.ques_score   
        user_answers = UserAnswer.objects.all().filter(
            user_id=self.request.user, question__quiz=page_number)     
        data = zip(quiz_questions, answers, user_answers)
        context_dictionary = {
            "quiz_number": page_number,
            "quiz_name": QuizModel.objects.filter(id=page_number).first(),
            "data": data,
            "total_score": total_score,
            "user_score": user_score,
            "incomplete": context["incomplete"]
        }
        for key, value in context_dictionary.items():
            context[key] = value
        return context



"""
Function based Approach

@login_required
def questionpage(request, page_number, name):
    #This view renders the template for display of each particular quiz.
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
    if len(user_answers) < len(quiz_questions):
        messages.warning(request, "Please attempt the whole quiz to continue")
        return redirect('home-quizzes')
    answers = Answer.objects.all().filter(question__quiz=page_number)
    total_score = 0
    user_score = 0
    for question in quiz_questions:
        total_score += question.ques_score
    for i in range(len(user_answers)):
        if user_answers[i].question.ques_type == "FIB":
            if user_answers[i].text == Answer.objects.filter(question_id=user_answers[i].question).first().solutions.lower():
                user_score += Question.objects.filter(
                    id=user_answers[i].question.id).first().ques_score
        elif user_answers[i].choice.is_correct:
            user_score += answers[i].question.ques_score
    context_dictionary = {
        "quiz_number": page_number,
        "quiz_name": name,
        "questions": quiz_questions,
        "user_answers": user_answers,
        "answers": answers,
        "total_score": total_score,
        "user_score": user_score
    }
    
Earlier Approach to render result page for scoring

    for i in range(len(user_answers)):
        if user_answers[i].question.ques_type == "FIB":
            if user_answers[i].text == Answer.objects.filter(question_id=user_answers[i].question).first().solutions.lower():
                user_score += Question.objects.filter(
                    id=user_answers[i].question.id).first().ques_score
        elif user_answers[i].choice.is_correct:
            user_score += user_answers[i].question.ques_score
"""
