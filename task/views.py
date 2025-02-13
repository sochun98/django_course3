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


class TodoDetailView(View):
    
    def get(self, request, pk):
        return render(request, "task/todo/detail.html")


class TodoUpdateView(View):
    
    def get(self, request, pk):
        return render(request, "task/todo/update.html")