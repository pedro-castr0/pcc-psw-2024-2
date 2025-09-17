# seu_projeto/comments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Count, Q

@login_required
# Apenas usuários com permissão de 'adicionar comentário' podem acessar esta view.
@permission_required('comments.add_comment', raise_exception=True)
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
# Apenas usuários com permissão de 'modificar comentário' podem acessar.
@permission_required('comments.change_comment', raise_exception=True)
def edit(request, id):
    comment = get_object_or_404(Comment, id=id)

    # Verificação extra: garante que apenas o autor do comentário ou um superusuário pode editá-lo.
    if not (request.user == comment.author or request.user.is_superuser):
        return HttpResponseForbidden("Você não tem permissão para editar este comentário.")

    posts = Post.objects.all()
    comments = Comment.objects.all()

    if request.method == 'POST':
        comment.content = request.POST.get('content')
        post_id = request.POST.get('post')
        comment.post = Post.objects.get(id = post_id)
        parent_id = request.POST.get('parent')
        comment.parent = Comment.objects.get(id = parent_id) if parent_id else None

        comment.save()

        return redirect('/comment/list/')
    
    return render(request, 'comment/form.html', {'comment':comment, 'comments':comments, 'posts':posts})

@login_required
# Qualquer usuário logado pode ver um comentário individual.
# Se precisar restringir, descomente a linha abaixo.
# @permission_required('comments.view_comment', raise_exception=True)
def view(request, id):
    comment = get_object_or_404(Comment, id=id)
    
    replies = comment.replies.all()

    get_karma = User.objects.annotate(
        karma=Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=True))
            - Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=False))
        ).get(id=comment.author.id)

    return render(request, 'comment/view.html', {'comment':comment, 'replies':replies, 'get_karma': get_karma, 'hide_view_button':True})


@login_required
# Apenas usuários com permissão de 'deletar comentário' podem acessar.
@permission_required('comments.delete_comment', raise_exception=True)
def delete(request, id):
    comment = get_object_or_404(Comment, id=id)

    # Verificação extra: garante que apenas o autor ou um superusuário pode deletar.
    if not (request.user == comment.author or request.user.is_superuser):
        return HttpResponseForbidden("Você não tem permissão para deletar este comentário.")

    post_id = comment.post.id  # Salva o ID do post antes de deletar o comentário
    comment.delete()

    return redirect(reverse('view_post', kwargs={'id': post_id}))

@login_required
# Apenas usuários com permissão de 'ver comentário' podem acessar a lista completa.
@permission_required('comments.view_comment', raise_exception=True)
def list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/list.html', {'comments':comments})