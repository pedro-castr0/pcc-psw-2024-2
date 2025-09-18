from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Denuncia(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]

    MOTIVO_CHOICES = [
        ('conteudo_inapropriado', 'Conteúdo inapropriado'),
        ('spam', 'Spam'),
        ('discurso_odio', 'Discurso de ódio'),
        ('assedio', 'Assédio'),
        ('informacao_falsa', 'Informação falsa'),
        ('outro', 'Outro'),
    ]

    autor = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="denuncias"
    )
    motivo = models.CharField(
        max_length=50,
        choices=MOTIVO_CHOICES,
        null=False,
        blank=False,
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    conteudo = GenericForeignKey('content_type', 'object_id')

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pendente'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_resolucao = models.DateTimeField(null=True, blank=True)

    analisado_por = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="denuncias_analisadas"
    )

    def __str__(self):
        return f"Denúncia #{self.id} - {self.status} ({self.content_type} {self.object_id})"
