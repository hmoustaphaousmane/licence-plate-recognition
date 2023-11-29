# urls.py
#from django.contrib.auth.views import LoginView
from django.urls import path
from .views import MyLoginView

urlpatterns = [
    # ... autres URL ...
    path('login/', MyLoginView.as_view(), name='login'),
]
