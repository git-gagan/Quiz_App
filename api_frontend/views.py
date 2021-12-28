from django.shortcuts import render
from django.views.generic.base import TemplateView


class ApiHomeView(TemplateView):
    """
    Class based view to display Home Page of API
    """
    template_name = "api_frontend/home_page.html"
