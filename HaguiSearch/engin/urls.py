from django.urls import path
from .views import *
urlpatterns = [
    path('streaming', StreamingTemplateView.as_view(), name='streaming'),

]