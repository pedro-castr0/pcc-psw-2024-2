from django.http import JsonResponse
from django.shortcuts import render
from .models import Tag
from communities.models import Community
from posts.models import Post

def get_tags(request):
    tags = Tag.objects.all().values("id", "name")
    return JsonResponse(list(tags), safe=False)


