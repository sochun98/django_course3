from django.shortcuts import render
# from django.views import View
from django.views.generic import TemplateView, View
import random


class RandomNumberTemplateView(TemplateView):
    template_name = "random.html"


class RandomNumberView(View):
    def get(self, request):
        random_number = random.randint(1, 100)
        return render(request, "random.html", {"random": random_number})