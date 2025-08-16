from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

@login_required
def comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        post_id = request.POST.get('post')
        parent_id = request.POST.get('parent')
        
        post = get_object_or_404(Post, id=post_id)
        author = request.user
        
        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

        comment = Comment.objects.create(
            content=content,
            author=author,
            post=post,
            parent=parent
        )

        comment_html = render_to_string("post/comment_section.html", {"comment": comment})
        comments_count = post.comments.count()

        return JsonResponse({
            "status": "success", 
            "comment_html": comment_html, 
            "comments_count": comments_count,
            "parent_id": parent_id if parent else None  # Se for resposta, retorna o parent_id
        })
    
    return JsonResponse({"status": "error", "message": "Método não permitido."})

@login_required
def list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/list.html', {'comments':comments})

@login_required
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


@login_required
def delete(request, id):
    comment = Comment.objects.get(id = id)
    comment.delete()

    return redirect('/comment/list/')


