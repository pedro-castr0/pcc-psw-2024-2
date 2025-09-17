from django.shortcuts import render, redirect, get_object_or_404
# Seus modelos de outros apps (ajuste o caminho se necessário)
from communities.models import Community
from tags.models import Tag
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponseForbidden

# Criar um post é uma ação padrão para usuários logados.
# Nenhuma permissão extra é necessária aqui.
@login_required
@permission_required('posts.add_post', raise_exception=True)
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

    # Supondo que você tenha um formulário em 'post/partials/form.html'
    # Esta parte do código não foi fornecida, mas a lógica de criação está acima.
    return render(request, 'post/partials/form.html')

# A lista de todos os posts é uma view administrativa.
@login_required
<<<<<<< HEAD
@permission_required('posts.view_post', raise_exception=True)
=======
@permission_required('post.view_post', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def list(request):
    posts = Post.objects.all()
    return render(request, 'post/list.html', {'posts':posts})

# Apenas o autor OU um moderador com permissão pode editar.
@login_required
<<<<<<< HEAD
@permission_required('posts.change_post', raise_exception=True)
=======
@permission_required('post.change_post', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def edit(request, id):
    post = get_object_or_404(Post, id=id)
    tags = Tag.objects.all()

    # LÓGICA DE PERMISSÃO APRIMORADA:
    # Permite a edição se o usuário for o autor OU tiver a permissão geral.
    if post.author != request.user and not request.user.has_perm('post.change_post'):
        return HttpResponseForbidden("Você não tem permissão para editar este post.")

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

# Apenas o autor OU um moderador com permissão pode deletar.
@login_required
<<<<<<< HEAD
@permission_required('posts.delete_post', raise_exception=True)
=======
@permission_required('post.delete_post', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    community_name = post.community.name # Salva o nome da comunidade antes de deletar

    # LÓGICA DE PERMISSÃO APRIMORADA:
    # Permite a exclusão se o usuário for o autor OU tiver a permissão geral.
    if post.author == request.user or request.user.has_perm('post.delete_post'):
        post.delete()
    else:
        return HttpResponseForbidden("Você não tem permissão para deletar este post.")

    # CORREÇÃO DE BUG: Redireciona para a comunidade, não para o post deletado.
    # (Assumindo que você tenha uma URL nomeada 'view' no app 'communities')
    return redirect(reverse('communities:view', kwargs={'name': community_name}))

# Ver um post é uma ação padrão para usuários logados.
@login_required
@permission_required('posts.view_post', raise_exception=True)
def view(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(parent__isnull=True)

    get_karma = User.objects.annotate(
        karma=Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=True))
            - Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=False))
        ).get(id=post.author.id)

    return render(request, 'post/view.html', {'post': post, 'comments': comments, 'hide_posted':True, 'post_button_hide':True, 'get_karma':get_karma})