from django.http import JsonResponse
from django.shortcuts import render
from .models import Tag
from communities.models import Community
from posts.models import Post

def tag_autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        tags = Tag.objects.filter(name__icontains=query).values_list('name', flat=True)[:10]
        return JsonResponse(list(tags), safe=False)
    return JsonResponse([], safe=False)


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags/tags_list.html', {'tags': tags})

def search_tags(request):
    query = request.GET.get('q', '')
    tags = []
    posts = []
    communities = []

    if query:
        tags = Tag.objects.filter(name__icontains=query)

        posts = Post.objects.filter(tags__in=tags).distinct()

        communities = Community.objects.filter(tags__in=tags).distinct()

    return render(request, 'tags/tags_search.html', {
        'query': query,
        'tags': tags,
        'posts': posts,
        'communities': communities,
    })


