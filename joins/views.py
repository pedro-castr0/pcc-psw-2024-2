from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Community, Join

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

def unjoin(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        join = get_object_or_404(Join, community_id=community_id, user=request.user)
        join.delete()

        community = get_object_or_404(Community, id=community_id)
        members_count = community.members.count()
        return JsonResponse({'status': 'success', 'joined': False, 'members_count': members_count})
    
def list(request):
    joins = Join.objects.all()
    return render(request, 'join/list.html', {'joins':joins})

def joined(request):
    if request.user.is_authenticated:
        joined_communities = Join.objects.filter(user=request.user).select_related('community')
    else:
        joined_communities = []
    return {
        'joined_communities': joined_communities
    }