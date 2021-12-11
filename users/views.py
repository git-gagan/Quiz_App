import pyotp

from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView

from .models import CustomUser
from .forms import MyUserForm, OtpForm
from quizproject.settings import EMAIL_HOST_USER


def get_otp(request):
    """
    External Function for OTP generation and handling
    """
    email = request.POST.get('email')
    base32secret = pyotp.random_base32()
    totp = pyotp.TOTP(base32secret, digits=4, interval=120)
    real_otp = totp.now()
    sender = EMAIL_HOST_USER
    receiver = email
    message = f"""
                From: From {sender}
                #To: To {receiver}
                Hey Buddy, 
                Thanks for signing up. Your OTP is {real_otp}.
                It is valid for 2 minutes. Be quick!
                """
    try:
        send_mail(
            'OTP verification',
            message,
            sender,
            [receiver],
            fail_silently=False,
        )
    except:
        CustomUser.objects.filter(email=email).delete()
        msg = "<h1>Failed to send email Try again</h1><a href = '/'><button>Try again</button></a>"
        return HttpResponse(msg)
    return real_otp


class Home(TemplateView):
    """
    This view simply renders the home page for each User
    """
    template_name = "users/home.html"


class Register(View):
    """
    This view deals with new user registration.
    """

    def get(self, request):
        form = MyUserForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.POST.get("username")
            request.session["otp"] = get_otp(request)
            request.session["user"] = user
            return redirect("verification")
        return render(request, "users/register.html", {"form": form})


class Verification(View):
    """
    This view deals with rendering the OTP page and verifying the user
    """

    def get(self, request):
        try:
            verified_obj = CustomUser.objects.all().filter(
                username=request.session["user"]).first()
        except:
            return HttpResponse("<h3>Page Not found!!</h3>")
        if not verified_obj.is_verified:
            form = OtpForm()
            return render(request, "users/verification.html", {"form": form})
        logout(self.request)
        return redirect("login")

    def post(self, request):
        user_input = request.POST.get("otp")
        if user_input != request.session["otp"]:
            error = "Verification Failed! Try again."
            return HttpResponse(error)
        else:
            messages.success(
                request, f"Account created for {request.session['user']}")
            user_object = CustomUser.objects.all().filter(
                username=request.session["user"]).first()
            user_object.is_verified = True
            user_object.save()
            logout(self.request)
            return redirect("login")


class LoginUser(LoginView):
    """
    This inbuilt view renders the login page and takes care of validation and display
    """
    template_name = 'users/login.html'
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You are logged out! Login here!")
        logout(self.request)
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        current_user = self.request.POST.get("username")
        this_user = CustomUser.objects.filter(username=current_user).first()
        if this_user.is_verified:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            messages.warning(request, "You are not a verified User! Access denied!")
            return redirect("register")
        


"""
---Function based approach---
def register(request):
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.POST.get("username")
            request.session["otp"] = get_otp(request)
            request.session["user"] = user
            return redirect("verification")
    else:
        form = MyUserForm()
    return render(request, "users/register.html", {"form": form})
    
    def verification(request):
        try:
            verified_obj = CustomUser.objects.all().filter(
            username=request.session["user"]).first()
        except:
            return HttpResponse("<h3>Page Not found!!</h3>")
        if verified_obj != None and not verified_obj.is_verified:
            if request.method == 'POST':
                user_input = request.POST.get("otp")
                if user_input != request.session["otp"]:
                    error = "Verification Failed! Try again."
                    verified_obj = None
                    return HttpResponse(error)
                else:
                    messages.success(
                        request, f"Account created for {request.session['user']}")
                    verified_obj.is_verified = True
                    verified_obj.save()
                    verified_obj = None
                    return redirect("login")
            return render(request, "users/verification.html")
        else:
            return redirect("register")
"""
