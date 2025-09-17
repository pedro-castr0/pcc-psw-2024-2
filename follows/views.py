from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import User, Follow
from django.http import HttpResponse
from django.http import JsonResponse
from notification.models import Notification
from django.http import JsonResponse

@login_required
@permission_required('follows.add_follow', raise_exception=True)
def follow(request):
    if request.method == 'POST':
        followed_id = request.POST.get('followed_id')
        followed = User.objects.get(id=followed_id)
        follower = request.user

        if followed.id != follower.id:
            follow_obj, created = Follow.objects.get_or_create(
                followed=followed,
                follower=follower
            )

            if created:
                Notification.objects.create(
                    user=followed,
                    sender=follower,
                    message=f"começou a seguir você.",
                    type_icon="bx bxs-user-plus",
                    link=f"/perfil/{follower.id}/"
                )

        return JsonResponse({
            'status': 'success',
            'following': True,
            'followers_count': followed.followers.count()
        })

@login_required
@permission_required('follows.delete_follow', raise_exception=True)
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

@login_required
@permission_required('follows.view_follow', raise_exception=True)
def list(request):
    follows = Follow.objects.all()
    return render(request, 'follow/list.html', {'follows':follows})