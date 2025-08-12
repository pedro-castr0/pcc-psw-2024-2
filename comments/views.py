from django.shortcuts import render, redirect
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

def comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        author = User.objects.get(id = request.user.id)
        post_id = request.POST.get('post')
        post = Post.objects.get(id = post_id)
        parent_id = request.POST.get('parent')
        parent = Comment.objects.filter(id=parent_id).first()

        comment = Comment(
            content = content,
            author = author,
            post = post,
            parent = parent
        )

        comment.save()

    return redirect('/comment/list/')

def list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/list.html', {'comments':comments})

def edit(request, id):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    comment = Comment.objects.get(id = id)

    if request.method == 'POST':
        comment.content = request.POST.get('content')
        author_id = request.POST.get('author')
        comment.author = User.objects.get(id = author_id)
        post_id = request.POST.get('post')
        comment.post = Post.objects.get(id = post_id)
        parent_id = request.POST.get('parent')
        comment.parent = Comment.objects.get(id = parent_id)

        comment.save()

        return redirect('/comment/list/')
    
    return render(request, 'comment/form.html', {'comment':comment, 'comments':comments, 'posts':posts})


def delete(request, id):
    comment = Comment.objects.get(id = id)
    comment.delete()

    return redirect('/comment/list/')


