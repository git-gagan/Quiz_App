from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .utils import mail
from .models import CustomUser
from .forms import MyUserForm, OtpForm

class Home(TemplateView):
    """
    This view simply renders the home page for each User
    """
    template_name = "users/home.html"
    
    def get(self, request, *args, **kwargs):
        logout(self.request)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class Register(FormView):
    """
    This view deals with new user registration.
    """
    form_class = MyUserForm
    template_name = "users/register.html"
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("verification")

@method_decorator(never_cache, name='dispatch')
class Verification(View):
    """
    This view deals with rendering the OTP page and verifying the user
    """

    def get(self, request):
        verified_obj = CustomUser.objects.all().filter(username=self.request.user).first()
        if not verified_obj:
            return HttpResponse("<h3>Page Not found!!</h3>")
        if verified_obj.is_verified:
            return redirect("login")
        real_otp = verified_obj.get_otp()
        mail(verified_obj.email, real_otp)
        form = OtpForm()
        return render(request, "users/verification.html", {"form": form})
        
    def post(self, request):
        verified_obj = CustomUser.objects.all().filter(username=self.request.user).first()
        user_input = self.request.POST.get("otp")
        if verified_obj.verify_otp(user_input):
            messages.success(request, f"Account created for {verified_obj.username}")
            return redirect("home-quizzes")
        messages.warning(self.request, "Verification Failed! LogIn to try again!")
        return redirect("login")

@method_decorator(never_cache, name='dispatch')
class LoginUser(LoginView):
    """
    This inbuilt view renders the login page and takes care of validation and display
    """
    template_name = 'users/login.html'
    
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        if self.request.user.is_verified:
            messages.success(self.request, "Logged in Successfully!")
            return redirect("home-quizzes")
        messages.warning(self.request, "You are not a verified user. ACCESS denied!")
        return redirect("verification")
    


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
            
Earlier Code for verfication
    # def get(self, request):
    #     logout(self.request)
    #     form = MyUserForm()
    #     return render(request, "users/register.html", {"form": form})

    # def post(self, request):
    #     form = MyUserForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         return redirect("verification")
    #     return render(request, "users/register.html", {"form": form})
"""
