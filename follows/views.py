from django.shortcuts import redirect, render
from .models import User, Follow
from django.http import HttpResponse

def follow(request):
    if request.method == 'POST':
        followed_id = request.POST.get('followed_id')
        followed = User.objects.get(id=followed_id)
        follower = request.user

        if followed.id != follower.id:
            Follow.objects.create(
                followed=followed,
                follower=follower,
            )
            return redirect('/actions/list/')
        else:
            return HttpResponse("You can't follow yourself.")
    else:
        return HttpResponse("You've got any response.")

<<<<<<< HEAD
def unfollow(request):
    followed_id = request.POST.get('followed_id')
    follow = Follow.objects.get(followed_id = followed_id, follower_id = request.user.id)
=======
def unfollow(request, id):
    follow = Follow.objects.get(followed_id = id, follower_id = request.user.id)
>>>>>>> 02e8a9abc387fbd5eb303a72e2516d70fbeeadfb
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
