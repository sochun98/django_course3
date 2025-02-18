from django.urls import path
from users.apis import SignupAPI


# 127.0.0.1:8080/api/auth/
urlpatterns = [
    path("signup/", SignupAPI.as_view()),
]