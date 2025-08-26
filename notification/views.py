from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification
from django.utils import timezone
from datetime import timedelta



@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Marca como lidas
    notifications.filter(read=False).update(read=True)

    data = []
    for n in notifications:
        # Link do usuário: se tiver remetente, aponta para o perfil dele; senão '#'
        user_link = f"/user/profile/{n.sender.username}/" if n.sender else "#"

        data.append({
            "user_name": n.sender.username if n.sender else "Sistema",
            "user_image": n.sender.profile.profile_picture.url if n.sender and n.sender.profile.profile_picture else "/static/assets/images/users/default.png",
            "type_icon": getattr(n, "type_icon", "bx bxs-bell"),
            "message": n.message,
            "link": user_link,
            "time": tempo_relativo(n.created_at)
        })

    return JsonResponse({"notifications": data, "count": notifications.count()})


def tempo_relativo(dt):
    """
    Recebe um datetime e retorna uma string representando o tempo
    relativo, como '5 minutos atrás', '2 horas atrás', etc.
    """
    if not dt:
        return "Desconhecido"

    now = timezone.now()
    delta = now - dt

    if delta < timedelta(minutes=1):
        return "Agora"
    elif delta < timedelta(hours=1):
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes} minuto{'s' if minutes > 1 else ''} atrás"
    elif delta < timedelta(days=1):
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hora{'s' if hours > 1 else ''} atrás"
    elif delta < timedelta(days=7):
        days = delta.days
        return f"{days} dia{'s' if days > 1 else ''} atrás"
    elif delta < timedelta(days=30):
        weeks = delta.days // 7
        return f"{weeks} semana{'s' if weeks > 1 else ''} atrás"
    elif delta < timedelta(days=365):
        months = delta.days // 30
        return f"{months} mês{'es' if months > 1 else ''} atrás"
    else:
        years = delta.days // 365
        return f"{years} ano{'s' if years > 1 else ''} atrás"