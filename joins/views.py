from django.http import JsonResponse, HttpResponseForbidden
# Importação atualizada para incluir permission_required
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Community, Join
from django.urls import reverse

# Esta view está correta. A ação de entrar numa comunidade
# deve estar disponível para qualquer usuário logado.
@login_required
def join(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        community = get_object_or_404(Community, id=community_id)
        user = request.user

        Join.objects.get_or_create(
            community=community,
            user=user
        )

        members_count = community.members.count()
        return JsonResponse({'status': 'success', 'joined': True, 'members_count': members_count})

# Esta view também está correta. A lógica já garante que
# o usuário só pode remover a si mesmo de uma comunidade.
@login_required
def leave(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        join = get_object_or_404(Join, community_id=community_id, user=request.user)
        join.delete()

        community = get_object_or_404(Community, id=community_id)
        members_count = community.members.count()
        return JsonResponse({'status': 'success', 'joined': False, 'members_count': members_count})

# Apenas usuários com permissão para 'ver' joins podem acessar esta lista.
@login_required
@permission_required('join.view_join', raise_exception=True)
def list(request):
    joins = Join.objects.all()

    return render(request, 'join/list.html', {'joins':joins})

# Apenas usuários com permissão para 'deletar' um join (expulsar) podem acessar.
@login_required
@permission_required('join.delete_join', raise_exception=True)
def kick(request, id):
    join = get_object_or_404(Join, id=id)
    community = join.community

    # VERIFICAÇÃO DE SEGURANÇA CRÍTICA:
    # Apenas o criador da comunidade ou um superusuário pode expulsar alguém.
    if request.user != community.creator and not request.user.is_superuser:
        return HttpResponseForbidden("Você não tem permissão para expulsar membros desta comunidade.")

    join.delete()

    return redirect(reverse('view', kwargs={'name': community.name}))