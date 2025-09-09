from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Count, Q

@login_required
def comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        post_id = request.POST.get('post')
        parent_id = request.POST.get('parent')

        post = get_object_or_404(Post, id=post_id)
        author = request.user

        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

        Comment.objects.create(
            content=content,
            author=author,
            post=post,
            parent=parent
        )

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def edit(request, id):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    comment = get_object_or_404(Comment, id=id)

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

@login_required
def view(request, id):
    comment = get_object_or_404(Comment, id=id)
    
    replies = comment.replies.all()

    get_karma = User.objects.annotate(

        karma=Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=True))
            - Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=False))

        ).get(id=comment.author.id)

    return render(request, 'comment/view.html', {'comment':comment, 'replies':replies, 'get_karma': get_karma, 'hide_view_button':True})


@login_required
def delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()

    return redirect(reverse('view_post', kwargs={'id': comment.post.id}))

@login_required
def list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/list.html', {'comments':comments})

