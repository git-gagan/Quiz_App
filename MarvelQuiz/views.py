from django.http.response import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.http import HttpResponse, request
from .forms import MyUserForm

# Views here

def SignUp(request):
    """
    View for Registration Form display
    """
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("HomePage")
    else:
        form = MyUserForm()
    return render(request, "Registration_form.html",{"form":form})

def HomePage(request):
    return HttpResponse("Registration Done!")
    
    
    

