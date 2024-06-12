from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm


def posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/posts.html', {"posts": posts})

def comments(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'posts/comments.html', {"post": post, "comments": comments})

def create_comment(request, pk):
    post = Post.objects.get(id=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("posts:comments", pk=post.id)

    return render(request, 'posts/create_comment.html', {"form": form, "post": post})

def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save()
            return redirect("posts:posts")

    return render(request, 'posts/create_post.html', {"form": form})


def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("posts:posts")

    return render(request, 'posts/create_post.html', {'form': form})


def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        post.delete()
        return redirect("posts:posts")

    return render(request, 'posts/delete_post.html', {'post': post})
