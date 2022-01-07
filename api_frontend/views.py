from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache


@method_decorator(never_cache, name='dispatch')
class ApiHomeView(TemplateView):
    """
    Class based view to display Home Page of API
    """
    template_name = "api_frontend/home-page.html"


@method_decorator(never_cache, name='dispatch')
class ApiRegistrationView(TemplateView):
    """
    Class based view to deal with User Sign up and do some minimal validation
    """
    template_name = "api_frontend/registration-page.html"


@method_decorator(never_cache, name='dispatch')
class ApiLoginView(TemplateView):
    """
    Class based view to deal with User Login 
    """
    template_name = "api_frontend/login-page.html"


@method_decorator(never_cache, name='dispatch')
class ApiVerificationView(TemplateView):
    """
    Class based view to deal with OTP verification
    """
    template_name = "api_frontend/verification-page.html"


@method_decorator(never_cache, name='dispatch')
class ApiQuizzesView(TemplateView):
    """
    Class based view to display all the available quizzes with an option to attempt them
    """
    template_name = "api_frontend/quizzes-page.html"


@method_decorator(never_cache, name='dispatch')
class ApiQuestionsView(TemplateView):
    """
    The view renders one question per page depending upon the user/quiz/time
    """
    template_name = "api_frontend/question-page.html"


@method_decorator(never_cache, name='dispatch')
class ApiResultView(TemplateView):
    """
    The view renders one question per page depending upon the user/quiz/time
    """
    template_name = "api_frontend/result-page.html"
