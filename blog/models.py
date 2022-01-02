from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=180)
    github_link = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    title = models.CharField(max_length=180)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_user_id = models.ForeignKey(User)
    project_id = models.ForeignKey(Project)


class Stat(models.Model):
    action_name = models.CharField(max_length=100)
    number = models.IntegerField()
    last_action = models.DateTimeField()


class Comment(models.Model):
    description = models.TextField()
    post_id = models.ForeignKey(Post)
    auth_user_id = models.ForeignKey(User)


class LikeProject(models.Model):
    auth_user_id = models.ForeignKey(User)
    project_id = models.ForeignKey(Project)


class PostProject(models.Model):
    auth_user_id = models.ForeignKey(User)
    post_id = models.ForeignKey(Post)


class LikeComment(models.Model):
    auth_user_id = models.ForeignKey(User)
    comment_id = models.ForeignKey(Comment)

