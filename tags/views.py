from django.http import JsonResponse
from django.shortcuts import render
from .models import Tag
from communities.models import Community
from django.contrib.auth.decorators import login_required, permission_required
from posts.models import Post
# Importação necessária para o decorador.
from django.contrib.auth.decorators import login_required

@login_required
@permission_required('tags.view_tag')
def get_tags(request):
    tags = Tag.objects.all().values("id", "name")
    return JsonResponse(list(tags), safe=False)