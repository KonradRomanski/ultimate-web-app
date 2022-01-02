from django.urls import path

from . import views

urlpatterns = [
    path('post', views.post, name='post'),
    path('post.html', views.post, name='post'),

    path('about', views.about, name='about'),
    path('about.html', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('contact.html', views.contact, name='contact'),

    path('index', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('', views.index, name='index'),
]

