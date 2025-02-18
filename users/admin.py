from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "__str__", "id", "is_staff",
    ]
    
    fieldsets = (
        ("Profile", {
            "fields": (
                "username",
                "password",
                "name",
                "email",
                "phone_number",
                "profile",
                "birth_date"
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    """
    # UserAdmin의 기존 fieldsets에 새로운 필드들을 추가
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "name",
                "phone_number",
                "profile",
                "birth_date"
            ),
        }),
    )
    """