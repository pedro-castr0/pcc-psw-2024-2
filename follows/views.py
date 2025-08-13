from django.shortcuts import redirect, render
from .models import User, Follow
from django.http import HttpResponse
from django.http import JsonResponse

from django.http import JsonResponse

def follow(request):
    if request.method == 'POST':
        followed_id = request.POST.get('followed_id')
        followed = User.objects.get(id=followed_id)
        follower = request.user

        if followed.id != follower.id:
            Follow.objects.get_or_create(followed=followed, follower=follower)

        return JsonResponse({
            'status': 'success',
            'following': True,
            'followers_count': followed.followers.count()
        })

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

def list(request):
    follows = Follow.objects.all()
    return render(request, 'follow/list.html', {'follows':follows})

def following(request):
    if request.user.is_authenticated:
        following = Follow.objects.filter(follower=request.user).select_related('followed')
    else:
        following = []
    return {
        'following': following
    }
