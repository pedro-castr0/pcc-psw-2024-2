from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def get_notifications(request):
    # Pegando as notificações do usuário logado
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Marca como lidas
    notifications.filter(read=False).update(read=True)

    data = []
    for n in notifications:
        data.append({
            "user_name": n.sender.username if n.sender else "Sistema",
            "user_image": n.sender.profile.profile_picture.url if n.sender and n.sender.profile.profile_picture else "/static/assets/images/users/default.png",
            "type_icon": n.type_icon if hasattr(n, "type_icon") else "bx bxs-bell",
            "message": n.message,
            "link": n.link if hasattr(n, "link") and n.link else "#",
            "time": n.created_at.strftime('%Hh')
        })

    return JsonResponse({"notifications": data, "count": notifications.count()})
