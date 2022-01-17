from django.urls import path
from .views import ListPosts, ListAFewPosts, PostView, ListRepos, LikeView
from . import views

urlpatterns = [
    path('post/<int:pk>', PostView.as_view(), name='post'),

    path('about', views.about, name='about'),

    path('contact', views.contact, name='contact'),

    path('blog', ListPosts.as_view(), name='blog'),

    path('repositories', ListRepos.as_view(), name='repositories'),

    path('index', ListAFewPosts.as_view(), name='index'),

    path('like/<int:pk>', LikeView, name='like_post'),

    path('', ListAFewPosts.as_view(), name='index'),
]

