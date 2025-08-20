from django.urls import path
from . import views
app_name = "denuncia" 

urlpatterns = [
    path('painel/', views.painel_denuncias, name='painel_denuncias'),
    path('criar/<str:app_label>/<str:model_name>/<int:object_id>/', views.criar_denuncia, name='criar_denuncia'),
    path('resolver/<int:denuncia_id>/<str:acao>/', views.resolver_denuncia, name='resolver_denuncia'),
]
