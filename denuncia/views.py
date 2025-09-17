from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
=======
# Importação atualizada para incluir o permission_required
from django.contrib.auth.decorators import login_required, permission_required
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Denuncia
from .forms import DenunciaForm
from django.http import JsonResponse
from django.apps import apps

# Esta view permanece apenas com @login_required, pois qualquer usuário logado
# deve ser capaz de fazer uma denúncia.
@login_required
@permission_required('denuncia.add_denuncia', raise_exception=True)
def criar_denuncia(request, app_label, model_name, object_id):
    model_class = apps.get_model(app_label=app_label, model_name=model_name)
    conteudo = get_object_or_404(model_class, id=object_id)

    if request.method == "POST":
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.content_type = ContentType.objects.get_for_model(model_class)
            denuncia.object_id = conteudo.id
            denuncia.autor = request.user # Adicionado autor da denúncia
            denuncia.save()
            return JsonResponse({"mensagem": "Denúncia enviada com sucesso!"})
        else:
            return JsonResponse({"erro": form.errors.as_json()}, status=400)

    form = DenunciaForm()
    html = render_to_string("denuncia/form_denuncia.html", {"form": form}, request=request)
    return JsonResponse({"html": html})


<<<<<<< HEAD
@login_required
@user_passes_test(lambda u: u.is_staff or u.has_perm('user.gerenciar_denuncias'))
=======
# Apenas usuários com a permissão para 'modificar denúncia' podem ver o painel.
@login_required
@permission_required('denuncia.change_denuncia', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def painel_denuncias(request):
    denuncias = Denuncia.objects.filter(status='pendente').select_related('autor')
    return render(request, "denuncia/painel.html", {"denuncias": denuncias})

<<<<<<< HEAD
@login_required
@user_passes_test(lambda u: u.is_staff or u.has_perm('user.gerenciar_denuncias'))
=======

# Apenas usuários com a permissão para 'modificar denúncia' podem resolver uma.
@login_required
@permission_required('denuncia.change_denuncia', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def resolver_denuncia(request, denuncia_id, acao):
    denuncia = get_object_or_404(Denuncia, id=denuncia_id)
    denuncia.status = 'aprovada' if acao == 'aprovar' else 'rejeitada'
    denuncia.data_resolucao = now()
    denuncia.analisado_por = request.user if request.user.is_authenticated else None
    denuncia.save()

    if denuncia.status == 'aprovada':
        conteudo = denuncia.conteudo
        if conteudo:
            conteudo.delete()  

    return redirect("denuncia:painel_denuncias")