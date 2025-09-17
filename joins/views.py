from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Community, Join
from django.urls import reverse

@login_required
@permission_required('joins.add_join', raise_exception=True)
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

@login_required
@permission_required('joins.delete_join', raise_exception=True)
def leave(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        join = get_object_or_404(Join, community_id=community_id, user=request.user)
        join.delete()

        community = get_object_or_404(Community, id=community_id)
        members_count = community.members.count()
        return JsonResponse({'status': 'success', 'joined': False, 'members_count': members_count})
    
@login_required
@permission_required('joins.view_join', raise_exception=True)
def list(request):
    joins = Join.objects.all()

    return render(request, 'join/list.html', {'joins':joins})

@login_required
@permission_required('joins.delete_join', raise_exception=True)
def kick(request, id):
    join = get_object_or_404(Join, id=id)
    join.delete()

    return redirect(reverse('view_community', kwargs={'name': join.community.name}))

