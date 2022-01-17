from django.contrib import admin
from .models import Post, Project, Stat, Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Project)
admin.site.register(Stat)
admin.site.register(Comment)
