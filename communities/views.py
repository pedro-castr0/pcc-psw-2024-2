from django.shortcuts import render, redirect, get_object_or_404
from communities.models import Community, CommunityRule
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import CommunityRuleForm

# === Comunidades ===

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
            name=name,
            display_name=display_name,
            context=context,
            creator=creator,
            community_picture=community_picture,
            community_banner=community_banner
        )
        community.save()
        
        return redirect(reverse('view', kwargs={'name': community.name}))

@login_required
def edit(request, name):
    community = get_object_or_404(Community, name=name)

    if request.method == 'POST':
        community.name = request.POST.get('name')
        community.display_name = request.POST.get('display_name')
        community.context = request.POST.get('context')

        if request.FILES.get('community_picture'):
            community.community_picture = request.FILES['community_picture']
            
        if request.FILES.get('community_banner'):
            community.community_banner = request.FILES['community_banner']

        community.save()

        return redirect(reverse('view', kwargs={'name': community.name}))
    
    return render(request, 'community/form.html', {'community': community})

@login_required
def delete(request, name):
    community = get_object_or_404(Community, name=name)

    if request.user != community.creator:
        return redirect(reverse('view', kwargs={'name': community.name}))

    community.delete()

    # redirecionar para listagem de comunidades
    return redirect(reverse('list'))

@login_required
def view(request, name):
    community = get_object_or_404(Community, name=name)
    return render(request, 'community/view.html', {'community': community})

@login_required
def home(request, name):
    posts = Post.objects.filter(community__name=name).distinct()
    community = get_object_or_404(Community, name=name)
    return render(request, 'community/partials/home.html', {
        'posts': posts, 'community': community
    })

@login_required
def context(request, name):
    community = get_object_or_404(Community, name=name)
    return render(request, 'community/partials/context.html', {
        'community': community
    })

@login_required
def post(request, name):
    community = get_object_or_404(Community, name=name)
    tags = Tag.objects.all()
    return render(request, 'post/form.html', {
        'community': community, 'tags': tags
    })

@login_required
def list(request):
    communities = Community.objects.all()
    return render(request, 'community/list.html', {'communities': communities})

# === Regras da Comunidade ===

@login_required
def add_rule(request, name):
    community = get_object_or_404(Community, name=name)

    if request.user != community.creator:
        return redirect(reverse('view', kwargs={'name': community.name}))

    if request.method == "POST":
        form = CommunityRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.community = community
            rule.save()
            return redirect(reverse('view', kwargs={'name': community.name}))
    else:
        form = CommunityRuleForm()

    return render(request, "community/add_rule.html", {"form": form, "community": community})

@login_required
def edit_rule(request, name, rule_id):
    community = get_object_or_404(Community, name=name)
    rule = get_object_or_404(CommunityRule, id=rule_id, community=community)

    if request.user != community.creator:
        return redirect(reverse('view', kwargs={'name': community.name}))

    if request.method == "POST":
        form = CommunityRuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect(reverse('view', kwargs={'name': community.name}))
    else:
        form = CommunityRuleForm(instance=rule)

    return render(request, "community/edit_rule.html", {
        "form": form, "community": community, "rule": rule
    })

@login_required
def delete_rule(request, name, rule_id):
    community = get_object_or_404(Community, name=name)
    rule = get_object_or_404(CommunityRule, id=rule_id, community=community)

    if request.user != community.creator:
        return redirect(reverse('view', kwargs={'name': community.name}))

    if request.method == "POST":
        rule.delete()

    return redirect(reverse('view', kwargs={'name': community.name}))