from django.urls import path
from users.apis import SignupAPI, LoginAPI, LogoutAPI


# 127.0.0.1:8080/api/auth/
urlpatterns = [
    path("signup/", SignupAPI.as_view()),
    path("login/", LoginAPI.as_view(), name='login'),
    path("logout/", LogoutAPI.as_view()),
]