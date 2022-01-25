from django.contrib import admin
from .models import Post, Project, Comment
from django.contrib.admin.models import LogEntry


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_at', 'auth_user_id']
    list_filter = ['title', 'content', 'created_at', 'auth_user_id']
    search_fields = ['id', 'title', 'content', 'created_at', 'auth_user_id__username']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'github_link', 'created_at', 'post_id']
    list_filter = ['name', 'github_link', 'created_at', 'post_id']
    search_fields = ['id', 'name', 'created_at', 'post_id']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'auth_user_id', 'post_id']
    list_filter = ['id', 'description', 'auth_user_id', 'post_id']
    search_fields = ['id', 'description', 'auth_user_id', 'post_id']


class Logging(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LogEntry, Logging)
