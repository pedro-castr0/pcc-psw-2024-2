from django.shortcuts import render, redirect
from communities.models import Community
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'community/form.html')
        
    elif request.method == 'POST':
        name = request.POST.get('name')
        display_name = request.POST.get('display_name')
        context = request.POST.get('context')
        creator = request.user
        community_picture = request.FILES.get('community_picture')
        community_banner = request.FILES.get('community_banner')


        community = Community(

            name = name,
            display_name = display_name,
            context = context,
            creator = creator,
            community_picture = community_picture,
            community_banner = community_banner

        )

        community.save()

    return redirect('/community/list/')

@login_required
def list(request):
    communities = Community.objects.all()
    return render(request, 'community/list.html', {'communities':communities})

@login_required
def edit(request, id):
    community = Community.objects.get(id = id)

    if request.method == 'POST':
        community.name = request.POST.get('name')
        community.display_name = request.POST.get('display_name')
        community.context = request.POST.get('context')
        community.community_picture = request.FILES.get('community_picture')
        community.community_banner = request.FILES.get('community_banner')

        community.save()

        return redirect('/')
    
    return render(request, 'community/form.html', {'community':community})


@login_required
def delete(request, id):
    community = Community.objects.get(id = id)
    community.delete()

    return redirect('/')

@login_required
def view(request, id):
    community = Community.objects.get(id = id)

    following_ids = set(
        request.user.following.values_list('followed_id', flat=True)
    )

    community_ids = set(
        request.user.joined_communities.values_list('community_id', flat=True)
    )

    return render(request, 'community/view.html', {'community':community, 'following_ids':following_ids, 'community_ids':community_ids})

@login_required
def home(request, id):
    posts = Post.objects.filter(community_id=id).distinct()
    community = Community.objects.get(id=id)

    return render(request, 'community/partials/home.html', {
        'posts': posts, 'community':community
    })

@login_required
def context(request, id):
    community = Community.objects.get(id=id)

    return render(request, 'community/partials/context.html', {
        'community': community
    })

@login_required
def post(request, id):
    community = Community.objects.get(id=id)
    tags = Tag.objects.all()

    return render(request, 'post/partials/form.html', {
        'community': community, 'tags':tags
    })


