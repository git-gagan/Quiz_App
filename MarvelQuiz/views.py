from django import http
from django.http.response import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, request
from .forms import MyUserForm, LoggingForm
import pyotp
from .models import QuizModel, User
from django.core.mail import send_mail
# Views here

Email = ""
real_otp = 0
def SignUp(request):
    """
    View for Registration Form display and sending OTP
    """
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            # If form data is valid, send OTP and redirect to verification page
            form.save()
            global Email 
            Email = request.POST.get('email')
            base32secret = pyotp.random_base32()
            totp = pyotp.TOTP(base32secret, digits=4, interval=120)
            #print("TOTP-------------------------------",totp.now())
            global real_otp
            real_otp = totp.now()
            sender = "er.gaganraj@gmail.com"
            receiver = Email
            message = f"""
                        From: From {sender}
                        To: To {receiver}
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
                User.objects.filter(email=Email).delete()
                msg = "<h1>Failed to send email Try again</h1><a href = '/'><button>Try again</button></a>"
                return HttpResponse(msg)
            return HttpResponseRedirect("Verification")
    else:
        form = MyUserForm()
    return render(request, "Registration_form.html",{"form":form})

def OTP(request):
    """
    This view deals with OTP verification display
    """
    try:
        verified_obj = User.objects.get(email=Email)
    except:
        return HttpResponseNotFound("<h3>Page Not found!!</h3>")
    if not verified_obj.is_verified:
        if request.method == 'POST':
            user_input = request.POST.get("otp")
            if user_input != real_otp:
                User.objects.filter(email=Email).delete()
                error = "Verification Failed! Try again."
                return HttpResponse(error)
            else:
                msg = "Congrats!!! You are a verfied User! <a href='/Login'>Login Now</a>"
                verified_obj.is_verified = True
                verified_obj.save()
                return HttpResponse(msg)
        return render(request, "Verification.html")
    else:
        return HttpResponseRedirect("/Login")
    
def LogIn(request):
    """
    This view deals with the login functionality verifying the credentials of the user.
    """
    if request.method == "POST":
        form = LoggingForm(request.POST)
        this_user = request.POST.get("user_name")
        this_user_pass = request.POST.get("password")
        if User.objects.all().filter(user_name=this_user, password=this_user_pass):
            return HttpResponseRedirect("/Home")
        else:
            return HttpResponse("Invalid Credentials")
    else:
        form = LoggingForm()
    return render(request, "LogInform.html", {"form":form}) 
    
def Home(request):
    """
    Home view here deals with the display and logic behind the HomePage
    It's showing all the quizzes being created.
    """
    all_quizzes = QuizModel.objects.all()
    return render(request, "HomePage.html", {"quizzes":all_quizzes})