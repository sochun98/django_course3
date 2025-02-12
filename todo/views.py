from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from todo.models import Todo


def todo_list(request):
    todos = Todo.objects.all()
    
    search = request.GET.get("search")
    
    if search:
        todos = todos.filter(name__icontains=search)
    
    return render(request, "todo/todo.html", {"todos": todos})


def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(id=pk)
    except Todo.DoesNotExist:
        return HttpResponse("없는 페이지입니다.", status=404)
    return render(request, "todo/todo.html", {"todo": todo})


def todo_detail_name(request, name):
    todo = Todo.objects.filter(name__icontains=name)
    first = todo.first()
    last = todo.last()
    return render(request, "todo/todo.html", {"todo": todo, "first": first, "last": last})


class TodoCreateView(View):
    
    def get(self, request):
        return render(request, "todo/create.html")


class TodoListView(View):
    
    def get(self, request):
        return render(request, "todo/list2.html")


class TodoDetailView(View):
    
    def get(self, request, pk):
        return render(request, "todo/detail.html")


class TodoUpdateView(View):
    
    def get(self, request, pk):
        return render(request, "todo/update.html")
