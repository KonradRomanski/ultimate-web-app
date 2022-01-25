from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from blog.forms import NewUserForm, CommentForm
from .models import Post, Project, LikePost, Comment, LikeProject, LikeComment


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


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
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
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


class ListPosts(ListView):
    queryset = Post.objects.order_by('created_at')
    model = Post
    template_name = 'blog/blog.html'


class ListAFewPosts(ListView):
    queryset = Post.objects.order_by('created_at')[:3]
    model = Post
    template_name = 'blog/index.html'


@login_required()
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


# def LikeView(request, pk):
#     post_likes = get_object_or_404(LikePost, id=request.get('post_id'))
#     post_likes.auth_user.add(request.user)
#     return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


@login_required
def PostDetail(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = get_user(request)
    comments = Comment.objects.filter(post_id=post.id)
    request.post_id = pk
    post.liked = 1 if LikePost.objects.filter(post_id=post.id, auth_user_id=get_user(request).id) else 0
    for c in comments:
        c.liked = 1 if LikeComment.objects.filter(comment_id=c.id, auth_user_id=get_user(request).id) else 0

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

@login_required
def ProjectDetail(request, pk):
    project = get_object_or_404(Project, id=pk)
    user = get_user(request)
    comments = Comment.objects.filter(pk=project.id)
    request.project_id = pk
    project.liked = 1 if LikeProject.objects.filter(project_id=pk, auth_user_id=get_user(request).id) else 0

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.project_id = project.id
            new_comment.auth_user_id = user.id
            new_comment.save()
            return redirect(f'./{pk}')
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/project.html', {'project': project, 'comments': comments, 'comment_form': comment_form})



@login_required
def LikeThisPost(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = get_user(request)
    post_liked = LikePost.objects.filter(post_id=post.id, auth_user_id=get_user(request).id)
    request.post_id = pk
    if request.method == 'POST':
        if not post_liked:
            new_like = LikePost()
            new_like.post_id = post.id
            new_like.auth_user_id = user.id
            new_like.save()
        else:
            post_liked.delete()
    return redirect(f'../{pk}')


@login_required
def LikeThisComment(request, pk, cpk):
    print(f"[CHECK] {pk} {cpk}")
    comment = get_object_or_404(Comment, id=cpk)
    user = get_user(request)
    comment_liked = LikeComment.objects.filter(comment_id=comment.id, auth_user_id=get_user(request).id)
    request.comment_id = cpk
    if request.method == 'GET':
        if not comment_liked:
            print("[GO]")
            new_like = LikeComment()
            new_like.comment_id = comment.id
            new_like.auth_user_id = user.id
            new_like.save()
        else:
            comment_liked.delete()
    return redirect(f'../../{pk}')

@login_required
def LikeThisProject(request, pk):
    project = get_object_or_404(Project, id=pk)
    user = get_user(request)
    project_liked = LikeProject.objects.filter(project_id=project.id, auth_user_id=get_user(request).id)
    request.project_id = pk
    if request.method == 'POST':
        if not project_liked:
            new_like = LikeProject()
            new_like.project_id = project.id
            new_like.auth_user_id = user.id
            new_like.save()
        else:
            project_liked.delete()
    return redirect(f'../{pk}')

