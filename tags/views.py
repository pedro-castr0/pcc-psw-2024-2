from django.http import JsonResponse
from django.shortcuts import render
from .models import Tag
from communities.models import Community
from posts.models import Post
# Importação necessária para o decorador.
from django.contrib.auth.decorators import login_required

# Adicionado @login_required para garantir que apenas usuários
# autenticados possam obter a lista de tags.
@login_required
def get_tags(request):
    tags = Tag.objects.all().values("id", "name")
    return JsonResponse(list(tags), safe=False)