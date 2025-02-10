from django.urls import path
from task.apis import TodoCreateAPI, TodoDeleteAPI, TodoListAPI, TodoRetrieveAPI, TodoUpdateAPI

# http://127.0.0.1:8000/api/task/
urlpatterns = [
    path("todo/create/", TodoCreateAPI.as_view()),
    path("todo/list/", TodoListAPI.as_view()),
    path("todo/retrieve/<int:pk>/", TodoRetrieveAPI.as_view()),
    path("todo/update/<int:pk>/", TodoUpdateAPI.as_view()),
    path("todo/delete/<int:pk>/", TodoDeleteAPI.as_view()),
]