from django.contrib import admin

from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for managing Post model, with customizable list display, filters, and search."""

    list_display = ["id", "title", "author", "status"]
    list_filter = (
        "author",
        "status",
    )
    search_fields = ("title", "content")
    ordering = ("created_date",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing Category model."""

    pass
