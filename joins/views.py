from django.shortcuts import redirect, render
from .models import Join, Community
from django.shortcuts import get_object_or_404


def join(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        community = Community.objects.get(id = community_id)
        user = request.user

        join = Join(
            community = community,
            user = user,
        )

        join.save()

        return redirect('/associate/list/')

def unjoin(request):
    if request.method == "POST":
        community_id = request.POST.get("community_id")
        join = get_object_or_404(Join, community_id=community_id, user=request.user)
        join.delete()

    return redirect('/associate/list/')
    
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