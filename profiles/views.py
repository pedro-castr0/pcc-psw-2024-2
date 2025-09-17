from django.shortcuts import render, redirect
from profiles.models import Profile
from comments.models import Comment
from posts.models import Post
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
<<<<<<< HEAD
=======
# Importação atualizada para incluir permission_required
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.db.models import Count, Q

# A lógica desta view é para um usuário editar o *seu próprio* perfil.
# @login_required é suficiente e seguro.
@login_required
@permission_required('profiles.change_profile', raise_exception=True)
def edit(request):
    user = request.user
    profile = get_object_or_404(Profile, user__username=user.username)

    if request.method == 'POST':
        profile.display_name = request.POST.get('display_name')
        profile.bio = request.POST.get('bio')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        if request.FILES.get('profile_banner'):
            profile.profile_banner = request.FILES['profile_banner']

        profile.save()

        return redirect(reverse('view', kwargs={'username': user.username}))
    
    return render(request, 'profile/form.html', {'profile': profile})

# Ver o perfil de outro usuário é uma ação padrão para membros da comunidade.
# @login_required é suficiente.
@login_required
@permission_required('profiles.view_profile', raise_exception=True)
def view(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    is_following = profile.user.followers.filter(follower_id=request.user.id).exists()

    get_karma = User.objects.annotate(

        karma=Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=True))
             - Count("posts__feedback_posts", filter=Q(posts__feedback_posts__feedback=False))

        ).get(id=profile.user.id)

    return render(request, 'profile/view.html', {'profile': profile, 'is_following': is_following, 'get_karma':get_karma})

# As views parciais abaixo também são para visualização pública (entre usuários logados).
# Todas já estão corretamente protegidas com @login_required.
@login_required
@permission_required('profiles.view_profile', raise_exception=True)
def likes(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(feedback_posts__user=profile.user, feedback_posts__feedback=True).distinct()
    return render(request, 'profile/partials/posts.html', {'posts': posts})

@login_required
@permission_required('profiles.view_profile', raise_exception=True)
def dislikes(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(feedback_posts__user=profile.user, feedback_posts__feedback=False).distinct()
    return render(request, 'profile/partials/posts.html', {'posts': posts})

@login_required
@permission_required('profiles.view_profile', raise_exception=True)
def posts(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(author=profile.user).distinct()
    return render(request, 'profile/partials/posts.html', {'posts': posts})

@login_required
@permission_required('profiles.view_profile', raise_exception=True)
def comments(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    comments = Comment.objects.filter(author=profile.user).distinct()
    return render(request, 'profile/partials/comments.html', {'comments': comments, 'hide_comment_buttons': True})

# A lista de todos os perfis é uma view administrativa.
# Apenas usuários com a permissão 'view_profile' poderão acessá-la.
@login_required
@permission_required('profiles.view_profile', raise_exception=True)
def list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile/list.html', {'profiles':profiles})