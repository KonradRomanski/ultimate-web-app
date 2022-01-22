from django.contrib import admin
from .models import Post, Project, Stat, Comment
from django.contrib.auth.admin import UserAdmin


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_at', 'auth_user_id']
    list_filter = ['title', 'content', 'created_at', 'auth_user_id']
    search_fields = ['id', 'title', 'content', 'created_at', 'auth_user_id__username']


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Project)
admin.site.register(Stat)
admin.site.register(Comment)
