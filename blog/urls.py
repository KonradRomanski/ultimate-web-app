from django.urls import path
from .views import ListPosts, ListAFewPosts, PostView, ListRepos, LikeView, PostDetail
from . import views

urlpatterns = [
    # path('post/<int:pk>', PostView.as_view(), name='post'),

    path('post/<int:pk>', PostDetail, name='post'),
    path('post', PostDetail, name='post'),

    path('about', views.about, name='about'),

    path('contact', views.contact, name='contact'),

    path('blog', ListPosts.as_view(), name='blog'),

    path('repositories', ListRepos.as_view(), name='repositories'),

    path('like/<int:pk>', LikeView, name='like_post'),

    path('', ListAFewPosts.as_view(), name='index'),
]

