from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from communities.models import Community
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

def home(request):
    posts = Post.objects.all()
    communities = Community.objects.all()
    users = User.objects.all()

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

    return render(request, 'home/home.html', 
                  {'posts':posts, 'communities':communities, 'users':users,
                   'following_ids':following_ids, 'community_ids':community_ids,
                   'positive_feedbacks':positive_feedbacks,
                    'negative_feedbacks':negative_feedbacks})