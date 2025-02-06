from django.contrib import admin
from todo.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "created_at",
        "updated_at",
    ]