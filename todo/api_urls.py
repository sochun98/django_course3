from django.urls import include, path
from todo.apis import TodoCreateAPI, TodoDeleteAPI, TodoGenericsCreateAPI, TodoGenericsDeleteAPI, TodoGenericsListAPI, TodoGenericsListCreateAPI, TodoGenericsRetrieveAPI, TodoGenericsRetrieveUpdateDeleteAPI, TodoGenericsUpdateAPI, TodoListAPI, TodoRetrieveAPI, TodoUpdateAPI, TodoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", TodoViewSet)


# http://127.0.0.1:8000/api/todo/
urlpatterns = [
    # APIS
    path("viewsets/", include(router.urls)),
    path("generics/", TodoGenericsListCreateAPI.as_view()),
    path("generics/<int:pk>/", TodoGenericsRetrieveUpdateDeleteAPI.as_view()),
    path("generics/create/", TodoGenericsCreateAPI.as_view()),
    path("generics/list/", TodoGenericsListAPI.as_view()),
    path("generics/retrieve/<int:pk>/", TodoGenericsRetrieveAPI.as_view()),
    path("generics/update/<int:pk>/", TodoGenericsUpdateAPI.as_view()),
    path("generics/delete/<int:pk>/", TodoGenericsDeleteAPI.as_view()),
    path("create/", TodoCreateAPI.as_view()),
    path("list/", TodoListAPI.as_view()),
    path("retrieve/<int:pk>/", TodoRetrieveAPI.as_view()),
    path("update/<int:pk>/", TodoUpdateAPI.as_view()),
    path("delete/<int:pk>/", TodoDeleteAPI.as_view()),
]