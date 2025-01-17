from django.contrib import admin
from ingredient.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name',]
    fields = ['name', 'description']
    search_fields = ['name', 'description']