from django.urls import path
from users.views import SignupView


# 127.0.0.1:8080/users/
urlpatterns = [
    path("signup/", SignupView.as_view(), name='signup'),
]
