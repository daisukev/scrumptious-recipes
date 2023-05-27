from django.contrib import admin

from .models import Recipe, Rating

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
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display=(
            "value",
            )
