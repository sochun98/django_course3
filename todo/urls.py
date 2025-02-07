from django.urls import path
from todo.apis import TodoCreateAPI, TodoDeleteAPI, TodoListAPI, TodoRetrieveAPI, TodoUpdateAPI
from todo.views import todo_list, todo_detail, todo_detail_name


# http://127.0.0.1:8000/todo/
urlpatterns = [
    path("create/", TodoCreateAPI.as_view()),
    path("list/", TodoListAPI.as_view()),
    path("retrieve/<int:pk>/", TodoRetrieveAPI.as_view()),
    path("update/<int:pk>/", TodoUpdateAPI.as_view()),
    path("delete/<int:pk>/", TodoDeleteAPI.as_view()),
    path("list/", todo_list),
    path("list/<int:pk>/", todo_detail),
    path("list/<str:name>/", todo_detail_name),
]