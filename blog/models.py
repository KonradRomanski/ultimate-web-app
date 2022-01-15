from django.db import models
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


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
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True)


class Stat(models.Model):
    class Meta:
        db_table = 'stat'

    action_name = models.CharField(max_length=100, primary_key=True)
    number = models.IntegerField()
    last_action = models.DateTimeField()


class Comment(models.Model):
    class Meta:
        db_table = 'comment'

    description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)


class LikeProject(models.Model):
    class Meta:
        db_table = 'like_project'
        unique_together = ('auth_user', 'project')

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class LikePost(models.Model):
    class Meta:
        db_table = 'like_post'
        unique_together = ('auth_user', 'post')

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class LikeComment(models.Model):
    class Meta:
        db_table = 'like_comment'
        unique_together = ('auth_user', 'comment')

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
