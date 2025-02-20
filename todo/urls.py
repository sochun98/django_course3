from django.urls import include, path
from todo.views import TodoCreateView, TodoDetailView, TodoListView, TodoUpdateView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register("", TodoViewSet)


# http://127.0.0.1:8000/todo/
urlpatterns = [
    # VIEWS
    path("create/", TodoCreateView.as_view()),
    path("list/", TodoListView.as_view(), name='todo_list'),
    path("<int:pk>/", TodoDetailView.as_view()),
    path("update/<int:pk>/", TodoUpdateView.as_view()),
    # path("<str:name>/", todo_detail_name),
]