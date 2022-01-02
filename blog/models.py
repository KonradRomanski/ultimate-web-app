from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    class Meta:
        db_table = 'project'
    name = models.CharField(max_length=180)
    github_link = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    class Meta:
        db_table = 'post'

    title = models.CharField(max_length=180)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_user = models.ForeignKey(User, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)


class Stat(models.Model):
    class Meta:
        db_table = 'stat'

    action_name = models.CharField(max_length=100)
    number = models.IntegerField()
    last_action = models.DateTimeField()


class Comment(models.Model):
    class Meta:
        db_table = 'comment'

    description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    auth_user = models.ForeignKey(User, on_delete=models.PROTECT)


class LikeProject(models.Model):
    class Meta:
        db_table = 'like_project'

    auth_user = models.ForeignKey(User, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)


class LikePost(models.Model):
    class Meta:
        db_table = 'like_post'

    auth_user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)


class LikeComment(models.Model):
    class Meta:
        db_table = 'like_comment'

    auth_user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)

