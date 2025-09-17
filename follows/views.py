from django.shortcuts import redirect, render
# Importação atualizada para incluir permission_required
from django.contrib.auth.decorators import login_required, permission_required
from .models import User, Follow
from django.http import HttpResponse, JsonResponse
from notification.models import Notification

# Esta view já está correta com @login_required, pois seguir é uma ação
# padrão para qualquer usuário autenticado.
@login_required
def follow(request):
    if request.method == 'POST':
        followed_id = request.POST.get('followed_id')
        followed = User.objects.get(id=followed_id)
        follower = request.user

        if followed.id != follower.id:
            # Cria o relacionamento de follow
            follow_obj, created = Follow.objects.get_or_create(
                followed=followed,
                follower=follower
            )

            if created:
                # Cria notificação usando sender
                Notification.objects.create(
                    user=followed,       # quem vai receber a notificação
                    sender=follower,     # quem está seguindo
                    message=f"começou a seguir você.",
                    type_icon="bx bxs-user-plus",  # opcional: ícone específico
                    link=f"/perfil/{follower.id}/"  # opcional: link para o perfil
                )

        return JsonResponse({
            'status': 'success',
            'following': True,
            'followers_count': followed.followers.count()
        })

# Esta view também está correta com @login_required. A lógica interna
# já garante que o usuário só pode dar unfollow em quem ele mesmo segue.
@login_required
def unfollow(request):
    if request.method == 'POST':
        followed_id = request.POST.get('followed_id')
        followed = User.objects.get(id=followed_id)
        Follow.objects.filter(followed=followed, follower=request.user).delete()

        return JsonResponse({
            'status': 'success',
            'following': False,
            'followers_count': followed.followers.count()
        })

# Apenas usuários com permissão para 'ver' follows podem acessar esta lista.
@login_required
@permission_required('follow.view_follow', raise_exception=True)
def list(request):
    follows = Follow.objects.all()
    return render(request, 'follow/list.html', {'follows':follows})