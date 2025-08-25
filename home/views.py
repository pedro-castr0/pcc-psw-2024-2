from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from communities.models import Community
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
def home(request):
    posts = Post.objects.all()
    communities = Community.objects.all()
    users = User.objects.all()

    return render(request, 'home/home.html', {
        'posts':posts, 'communities':communities, 'users':users
    })