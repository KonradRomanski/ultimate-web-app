from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
# Create your views here.
from blog.forms import NewUserForm, CommentForm
from .models import Post, Project, LikePost, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


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
    model = Post.objects.all()
    template_name = 'blog/blog.html'


class ListAFewPosts(ListView):
    queryset = Post.objects.order_by('created_at')[:3]
    model = Post
    template_name = 'blog/index.html'


class PostView(DetailView):
    model = Post
    template_name = 'blog/post.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context['commentform'] = CommentForm()
    #     return context
    #
    # def post(self, request, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     form = CommentForm(request.POST)
    #
    #     if form.is_valid():
    #         obj = form.save(commit=False)
    #         obj.post = post
    #         obj.author = self.request.user
    #         obj.save()
    #         return redirect('detail', post.pk)


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


@login_required
def PostDetail(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = get_user(request)
    comments = Comment.objects.filter(post_id=post.id)
    request.post_id = pk
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post_id = post.id
            new_comment.auth_user_id = user.id
            new_comment.save()
            return redirect(f'./{pk}')
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post.html', {'post': post, 'comments': comments, 'comment_form': comment_form})
