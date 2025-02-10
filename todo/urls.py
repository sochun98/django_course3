from django.urls import include, path
from todo.views import TodoCreateView, TodoListView, todo_list, todo_detail, todo_detail_name
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register("", TodoViewSet)


# http://127.0.0.1:8000/todo/
urlpatterns = [
    # VIEWS
    path("create/", TodoCreateView.as_view()),
    path("list/", TodoListView.as_view()),
    path("list/<int:pk>/", todo_detail),
    path("list/<str:name>/", todo_detail_name),
]