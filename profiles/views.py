from django.shortcuts import render, redirect
from .models import Profile
from follows.models import Follow
from django.contrib.auth.models import User


def update(request):
    if request.method == 'GET':
        return render(request, 'profile/form.html')
    
    elif request.method == 'POST':
        user_id = request.POST.get('user')
        user = User.objects.get(id = user_id) 
        display_name = request.POST.get('display_name')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')
        banner = request.FILES.get('banner')

        profile = Profile(
            user = user,
            display_name = display_name,
            bio = bio,
            profile_picture = profile_picture,
            banner = banner
        )

        profile.save()

        return redirect('/community/list/')
        
    return render(request, 'profile/form.html')

def view(request, id):
    profile = Profile.objects.get(id = id)

    is_following = profile.user.followers.filter(follower_id=request.user.id).exists()

    following_ids = set(
        request.user.following.values_list('followed_id', flat=True)
    )

    community_ids = set(
        request.user.joined_communities.values_list('community_id', flat=True)
    )

    positive_feedbacks = set(
        request.user.feedbacks.filter(feedback=True).values_list('post_id', flat=True)
    )

    negative_feedbacks = set(
        request.user.feedbacks.filter(feedback=False).values_list('post_id', flat=True)
    )

    return render(request, 'profile/view.html', {'profile': profile, 'is_following': is_following, 'following_ids':following_ids, 'community_ids':community_ids, 'positive_feedbacks':positive_feedbacks, 'negative_feedbacks':negative_feedbacks})

def list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile/list.html', {'profiles':profiles})

def delete(request, id):
    profile = Profile.objects.get(id = id)
    profile.delete()
