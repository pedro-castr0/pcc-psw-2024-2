from django.shortcuts import render, redirect, get_object_or_404
from .models import Community, Post
from comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

def create(request):
    if request.method == 'GET':
        communities = Community.objects.all()
        return render(request, 'post/form.html', {'communities':communities})
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag = request.POST.get('tag')
        author_id = request.POST.get('author')
        author = User.objects.get(id = author_id)
        community_id = request.POST.get('community')
        community = Community.objects.get(id = community_id) 

        post = Post(
            title = title,
            content = content,
            tag = tag,
            author = author,
            community = community
        )

        post.save()

    return redirect('/post/list/')

def list(request):
    posts = Post.objects.all()
    return render(request, 'post/list.html', {'posts':posts})

def edit(request, id):
    communities = Community.objects.all()
    post = Post.objects.get(id = id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.tag = request.POST.get('tag')
        community_id = request.POST.get('community')
        post.community = Community.objects.get(id = community_id)

        post.save()

        return redirect('/post/list/')
    
    return render(request, 'post/form.html', {'communities':communities, 'post':post})


def delete(request, id):
    post = Post.objects.get(id = id)
    post.delete()

    return redirect('/post/list/')

def view(request, id):
    post = Post.objects.get(id = id)
    comments = post.comments.filter(parent__isnull=True)

    positive_feedbacks = set(
        request.user.feedbacks.filter(feedback=True).values_list('post_id', flat=True)
    )

    negative_feedbacks = set(
        request.user.feedbacks.filter(feedback=False).values_list('post_id', flat=True)
    )
    
    return render(request, 'post/view.html', {'post': post, 'comments': comments, 'positive_feedbacks':positive_feedbacks, 'negative_feedbacks':negative_feedbacks})


