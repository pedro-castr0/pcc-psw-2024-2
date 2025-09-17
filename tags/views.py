from django.http import JsonResponse
from django.shortcuts import render
from .models import Tag
from communities.models import Community
from django.contrib.auth.decorators import login_required, permission_required
from posts.models import Post
# Importação necessária para o decorador.
from django.contrib.auth.decorators import login_required

<<<<<<< HEAD
@login_required
@permission_required('tags.view_tag')
=======
# Adicionado @login_required para garantir que apenas usuários
# autenticados possam obter a lista de tags.
@login_required
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def get_tags(request):
    tags = Tag.objects.all().values("id", "name")
    return JsonResponse(list(tags), safe=False)