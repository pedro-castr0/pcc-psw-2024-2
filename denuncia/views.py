from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Denuncia
from .forms import DenunciaForm
from django.http import JsonResponse
from django.apps import apps

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
            denuncia.save()
            return JsonResponse({"mensagem": "Denúncia enviada com sucesso!"})
        else:
            return JsonResponse({"erro": form.errors.as_json()}, status=400)

    form = DenunciaForm()
    html = render_to_string("denuncia/form_denuncia.html", {"form": form}, request=request)
    return JsonResponse({"html": html})


@login_required
@user_passes_test(lambda u: u.is_staff or u.has_perm('user.gerenciar_denuncias'))
def painel_denuncias(request):
    denuncias = Denuncia.objects.filter(status='pendente').select_related('autor')
    return render(request, "denuncia/painel.html", {"denuncias": denuncias})

@login_required
@user_passes_test(lambda u: u.is_staff or u.has_perm('user.gerenciar_denuncias'))
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


