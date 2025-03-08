from django.contrib import admin

from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status"]
    list_filter = ('author', 'status',)
    search_fields = ('title','content')
    ordering = ("created_date",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass