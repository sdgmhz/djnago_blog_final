from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["email", "post", "approved"]
    list_filter = ["email", "post", "recommend", "approved"]
    search_fields = ["subject", "message"]
