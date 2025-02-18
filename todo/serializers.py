from rest_framework import serializers
from todo.models import Todo
# from django.contrib.auth.models import User
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password", "is_superuser", "is_staff",
        )


class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Todo
        fields = "__all__"