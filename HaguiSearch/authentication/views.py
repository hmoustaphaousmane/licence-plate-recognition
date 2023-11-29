from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class MyLoginView(LoginView):
    template_name = 'login/signin.html'
    success_url = reverse_lazy('home')
