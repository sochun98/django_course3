from django.contrib import admin
from brand.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "website",
    ]