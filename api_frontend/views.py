from django.views.generic.base import TemplateView


class ApiHomeView(TemplateView):
    """
    Class based view to display Home Page of API
    """
    template_name = "api_frontend/home-page.html"


class ApiRegistrationView(TemplateView):
    """
    Class based view to deal with User Sign up and do some minimal validation
    """
    template_name = "api_frontend/registration-page.html"


class ApiLoginView(TemplateView):
    """
    Class based view to deal with User Login 
    """
    template_name = "api_frontend/login-page.html"

class ApiVerificationView(TemplateView):
    """
    Class based view to deal with OTP verification
    """
    template_name = "api_frontend/verification-page.html"

class ApiQuizzesView(TemplateView):
    """
    Class based view to display all the available quizzes with an option to attempt them
    """
    template_name = "api_frontend/quizzes-page.html"
