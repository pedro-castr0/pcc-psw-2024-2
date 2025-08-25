from django.shortcuts import render, redirect, get_object_or_404
from .models import Community, Post, Tag
from comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import reverse

@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        community_id = request.POST.get('community_id')
        community = get_object_or_404(Community, id=community_id)

        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            community=community
        )

        tag_ids = request.POST.getlist('post_tag')

        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.post_tag.set(tags)

        return redirect(reverse('view_post', kwargs={'id': post.id}))

    return render(request, 'post/partials/form.html')

@login_required
def list(request):
    posts = Post.objects.all()
    return render(request, 'post/list.html', {'posts':posts})

@login_required
def edit(request, id):
    post = get_object_or_404(Post, id=id)
    tags = Tag.objects.all()

    if post.author != request.user:
        return redirect(reverse('view_post', kwargs={'id': post.id}))

    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)

        post.save()

        tag_ids = request.POST.getlist('post_tag')

        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.post_tag.set(tags)

        return redirect(reverse('view_post', kwargs={'id': post.id}))

    return render(request, 'post/form.html', {'post': post, 'tags':tags})

@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author == request.user:
        post.delete()

    return redirect(reverse('view_post', kwargs={'name': post.community.name}))

@login_required
def view(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(parent__isnull=True)

    return render(request, 'post/view.html', {'post': post, 'comments': comments})


