# seu_projeto/comments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Count, Q
from .forms import CommentForm, EditCommentForm


@login_required
@permission_required('comments.add_comment', raise_exception=True)
def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user  
            new_comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@permission_required('comments.change_comment', raise_exception=True)
def edit(request, id):
    comment = get_object_or_404(Comment, id=id)

    # só autor ou superuser pode editar
    if not (request.user == comment.author or request.user.is_superuser):
        return HttpResponseForbidden("Você não tem permissão para editar este comentário.")

    if request.method == 'POST':
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
    else:
        form = EditCommentForm(instance=comment)

    replies = comment.replies.all()

    get_karma = User.objects.annotate(
        karma=Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=True))
            - Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=False))
        ).get(id=comment.author.id)
    
    return render(request, 'comment/editar_comentarios.html', {'form': form, 'comment':comment, 'replies':replies, 'get_karma': get_karma, 'hide_view_button':True})


@login_required
@permission_required('comments.view_comment', raise_exception=True)
def view(request, id):
    comment = get_object_or_404(Comment, id=id)
    
    replies = comment.replies.all()

    get_karma = User.objects.annotate(
        karma=Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=True))
            - Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=False))
        ).get(id=comment.author.id)

    return render(request, 'comment/view.html', {'comment':comment, 'replies':replies, 'get_karma': get_karma, 'hide_view_button':True})


@login_required
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
@permission_required('comments.view_comment', raise_exception=True)
def list(request):
    comments = Comment.objects.all()
    return render(request, 'comment/list.html', {'comments':comments})