from django.shortcuts import render, redirect
from profiles.models import Profile
from comments.models import Comment
from posts.models import Post
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def edit(request):
    user = request.user
    profile = get_object_or_404(Profile, user__username=user.username)

    if request.method == 'POST':
        profile.display_name = request.POST.get('display_name')
        profile.bio = request.POST.get('bio')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        if request.FILES.get('profile_banner'):
            profile.profile_banner = request.FILES['profile_banner']

        profile.save()

        return redirect(reverse('view', kwargs={'username': user.username}))
    
    return render(request, 'profile/form.html', {'profile': profile})

@login_required
def view(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    is_following = profile.user.followers.filter(follower_id=request.user.id).exists()

    return render(request, 'profile/view.html', {'profile': profile, 'is_following': is_following})

@login_required
def likes(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    posts = Post.objects.filter(feedback_posts__user=profile.user, feedback_posts__feedback=True).distinct()

    return render(request, 'profile/partials/posts.html', {
        'posts': posts,
    })

@login_required
def dislikes(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    posts = Post.objects.filter(feedback_posts__user=profile.user, feedback_posts__feedback=False).distinct()

    return render(request, 'profile/partials/posts.html', {
        'posts': posts,
    })

@login_required
def posts(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    posts = Post.objects.filter(author=profile.user).distinct()

    return render(request, 'profile/partials/posts.html', {
        'posts': posts,
    })

@login_required
def comments(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    comments = Comment.objects.filter(author=profile.user).distinct()

    return render(request, 'profile/partials/comments.html', {
        'comments': comments
    })

@login_required
def list(request):
    profiles = Profile.objects.all()
    
    return render(request, 'profile/list.html', {'profiles':profiles})

