from django.urls import path
from todo.views import todo_list, todo_detail, todo_detail_name


urlpatterns = [
    path("list/", todo_list),
    path("list/<int:pk>/", todo_detail),
    path("list/<str:name>/", todo_detail_name),
]