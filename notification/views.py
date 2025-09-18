from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Notification
from django.utils import timezone
from datetime import timedelta

@login_required
@permission_required('notification.view_notification', raise_exception=True)
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    notifications.filter(read=False).update(read=True)

    data = []
    for n in notifications:
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


@login_required
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
    # ... (resto da função)