from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class StreamingTemplateView(TemplateView):
    template_name = 'engin/index.html'