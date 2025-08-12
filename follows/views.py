from django.shortcuts import redirect, render
from .models import User, Follow

def follow(request):
    if request.method == 'POST':
        followed_id = request.POST.get('followed_id')
        followed = User.objects.get(id = followed_id)
        follower = request.user

        follow = Follow(
            followed = followed,
            follower = follower,
        )

        follow.save()

        return redirect('/actions/list/')

def unfollow(request, id):
    follow = Follow.objects.get(followed_id = id, follower_id = request.user.id)
    follow.delete()

    return redirect('/actions/list/')

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
