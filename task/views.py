from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from task.models import Todo


class TodoCreateView(View):
    
    def get(self, request):
        return render(request, "task/todo/create.html")


class TodoListView(View):
    
    def get(self, request):
        return render(request, "task/todo/list.html")