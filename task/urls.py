from django.urls import path
from task.apis import TodoCreateAPI, TodoDeleteAPI, TodoListAPI, TodoRetrieveAPI, TodoUpdateAPI
from task.views import TodoCreateView, TodoListView

# http://127.0.0.1:8000/task/
urlpatterns = [
    path("todo/create/", TodoCreateView.as_view()),
    path("todo/list/", TodoListView.as_view()),
]