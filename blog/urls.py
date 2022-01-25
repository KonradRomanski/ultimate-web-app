from django.urls import path
from .views import LikeThisComment, LikeThisProject, ListPosts, ListAFewPosts, PostView, ListRepos, PostDetail, LikeThisPost
from . import views

urlpatterns = [
    # path('post/<int:pk>', PostView.as_view(), name='post'),

    path('post/<int:pk>', PostDetail, name='post'),
    # path('post', PostDetail, name='post'),

    path('post/<int:pk>/like', LikeThisPost, name='post'),

    path('post/<int:pk>/<int:cpk>/like', LikeThisComment, name='post'),

    path('repositories/<int:pk>/like', LikeThisProject, name='post'),

    path('about', views.about, name='about'),

    path('blog', ListPosts.as_view(), name='blog'),

    path('repositories', ListRepos.as_view(), name='repositories'),

    # path('like/<int:pk>', LikeView, name='like_post'),

    path('', ListAFewPosts.as_view(), name='index'),
]

