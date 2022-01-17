from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
# Create your views here.
from blog.forms import NewUserForm
from .models import Post, Project, LikePost
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def index(request):
    return render(request, 'blog/index.html')


def post(request):
    return render(request, 'blog/post.html')

def blog(request):
    return render(request, 'blog/blog.html')

def repositories(request):
    return render(request, 'blog/repositories.html')

def post_comment(request):
    return

def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/blog")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="blog/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("blog/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form": form})



class ListPosts(ListView):
    model = Post
    template_name = 'blog/blog.html'


class ListAFewPosts(ListView):
    queryset = Post.objects.order_by('created_at')[:1]
    model = Post
    template_name = 'blog/index.html'

class PostView(DetailView):
    model = Post
    template_name = 'blog/post.html'


class ListRepos(ListView):
    model = Project
    template_name = 'blog/repositories.html'

def LikeView(request, pk):
    post_likes = get_object_or_404(LikePost, id=request.get('post_id'))
    post_likes.auth_user.add(request.user)
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/blog")

