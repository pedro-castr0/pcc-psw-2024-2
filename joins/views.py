from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Community, Join
from django.urls import reverse

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

@login_required
def leave(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        join = get_object_or_404(Join, community_id=community_id, user=request.user)
        join.delete()

        community = get_object_or_404(Community, id=community_id)
        members_count = community.members.count()
        return JsonResponse({'status': 'success', 'joined': False, 'members_count': members_count})
    
@login_required
def list(request):
    joins = Join.objects.all()

    return render(request, 'join/list.html', {'joins':joins})

@login_required
def kick(request, id):
    join = get_object_or_404(Join, id=id)
    join.delete()

    return redirect(reverse('view_community', kwargs={'name': join.community.name}))

