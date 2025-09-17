from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from communities.models import Community
from tags.models import Tag
from django.contrib.auth.models import User
# A importação já inclui o login_required, que é o que precisamos aqui.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Esta view já estava correta, garantindo que a página inicial
# só pode ser vista por usuários logados.
@login_required
def home(request):
    posts = Post.objects.all()
    communities = Community.objects.all()
    users = User.objects.all()
    tags = Tag.objects.all()

    return render(request, 'home/home.html', {
        'posts':posts, 'communities':communities, 'users':users, 'tags':tags
    })

<<<<<<< HEAD
=======
# Adicionado @login_required para garantir que apenas usuários
# autenticados possam realizar buscas.
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    selected_tags = request.GET.getlist('tags')

    posts = Post.objects.all()
    users = User.objects.none()
    communities = Community.objects.none()

    if query:
        posts = posts.filter(title__icontains=query).distinct()
        users = User.objects.filter(username__icontains=query)[:10]
        communities = Community.objects.filter(name__icontains=query)

    if selected_tags:
        posts = posts.filter(post_tag__id__in=selected_tags).distinct()

    return render(request, 'home/home.html', {
        'query': query,
        'posts': posts,
        'communities': communities,
        'users': users,
        'selected_tags': list(map(int, selected_tags)),  # para manter o estado dos checkboxes
    })

<<<<<<< HEAD
=======
# Adicionado @login_required para proteger o endpoint de autocomplete
# contra acesso não autenticado.
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
@login_required
def autocomplete(request):
    query = request.GET.get('q', '')
    results = {
        'users': [],
        'communities': [],
        'posts': []
    }

    if query:
        results['users'] = list(
            User.objects.filter(username__icontains=query)
            .values_list('username', flat=True)[:3]
        )

        results['communities'] = list(
            Community.objects.filter(name__icontains=query)
            .values_list('name', flat=True)[:3]
        )

        results['posts'] = list(
            Post.objects.filter(title__icontains=query)
            .values_list('title', flat=True)[:3]
        )

    return JsonResponse(results, safe=False)