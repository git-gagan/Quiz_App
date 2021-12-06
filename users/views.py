from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import MyUserForm
from django.contrib import messages
from django.core.mail import send_mail
from .models import CustomUser
import pyotp


def get_otp(request):
    email = request.POST.get('email')
    base32secret = pyotp.random_base32()
    totp = pyotp.TOTP(base32secret, digits=4, interval=120)
    real_otp = totp.now()
    sender = "er.gaganraj@gmail.com"
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
    
class LoginUser(LoginView):
    template_name = 'users/login.html'
    
        