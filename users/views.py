from django.shortcuts import redirect, render
from .forms import MyUserForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.POST.get("username")
            messages.success(request, f"Account created for {user}")
            return redirect("home-quizzes")
    else:
        form = MyUserForm()
    return render(request, "users/register.html", {"form": form})
