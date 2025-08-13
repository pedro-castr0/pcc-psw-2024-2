from django.shortcuts import render, redirect
from profiles.models import Profile
from comments.models import Comment
from posts.models import Post
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


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

    return render(request, 'profile/view.html', {'profile': profile, 'is_following': is_following, 'following_ids':following_ids, 'community_ids':community_ids})

def likes(request, id):
    profile = Profile.objects.get(id=id)

    posts = Post.objects.filter(feedback_posts__user=profile.user, feedback_posts__feedback=True).distinct()

    feedbacks = request.user.feedbacks.values('post_id', 'feedback')

    positive_feedbacks = {f['post_id'] for f in feedbacks if f['feedback']}
    negative_feedbacks = {f['post_id'] for f in feedbacks if not f['feedback']}

    return render(request, 'profile/partials/posts.html', {
        'posts': posts,
        'positive_feedbacks': positive_feedbacks,
        'negative_feedbacks': negative_feedbacks
    })

def dislikes(request, id):
    profile = Profile.objects.get(id=id)

    posts = Post.objects.filter(feedback_posts__user=profile.user, feedback_posts__feedback=False).distinct()

    feedbacks = request.user.feedbacks.values('post_id', 'feedback')

    positive_feedbacks = {f['post_id'] for f in feedbacks if f['feedback']}
    negative_feedbacks = {f['post_id'] for f in feedbacks if not f['feedback']}

    return render(request, 'profile/partials/posts.html', {
        'posts': posts,
        'positive_feedbacks': positive_feedbacks,
        'negative_feedbacks': negative_feedbacks
    })

def posts(request, id):
    profile = Profile.objects.get(id=id)

    posts = Post.objects.filter(author=profile.user).distinct()

    feedbacks = request.user.feedbacks.values('post_id', 'feedback')

    positive_feedbacks = {f['post_id'] for f in feedbacks if f['feedback']}
    negative_feedbacks = {f['post_id'] for f in feedbacks if not f['feedback']}

    return render(request, 'profile/partials/posts.html', {
        'posts': posts,
        'positive_feedbacks': positive_feedbacks,
        'negative_feedbacks': negative_feedbacks
    })

def comments(request, id):
    profile = Profile.objects.get(id=id)

    comments = Comment.objects.filter(author=profile.user).distinct()

    return render(request, 'profile/partials/comments.html', {
        'comments': comments
    })

def list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile/list.html', {'profiles':profiles})

def delete(request, id):
    profile = Profile.objects.get(id = id)
    profile.delete()
