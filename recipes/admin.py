from django.contrib import admin

from .models import Recipe

# Register your models here.
# Version 1
# admin.site.register(Recipe)

# Version 2
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display=(
            "title",
            "id",
            "description"
            )
