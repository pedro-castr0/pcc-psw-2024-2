from django.shortcuts import redirect, get_object_or_404, render
<<<<<<< HEAD
=======
# Importação atualizada para incluir o permission_required
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
from django.contrib.auth.decorators import login_required, permission_required
from .models import Post, Feedback
from django.http import JsonResponse

<<<<<<< HEAD
@login_required
@permission_required('feedback.add_feedback', raise_exception=True)
=======
# Adicionado @login_required para garantir que apenas usuários logados possam dar feedback.
@login_required
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def feedback(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        feedback_type = request.POST.get('feedback')
        user = request.user

        post = get_object_or_404(Post, id=post_id)

        is_like = True if feedback_type == 'like' else False

        fb_obj, created = Feedback.objects.update_or_create(
            user=user,
            post=post,
            defaults={'feedback': is_like}
        )

        post.likes_count = post.feedback_posts.filter(feedback=True).count()
        post.dislikes_count = post.feedback_posts.filter(feedback=False).count()
        post.save()

        liked = post.feedback_posts.filter(user=user, feedback=True).exists()
        disliked = post.feedback_posts.filter(user=user, feedback=False).exists()

        return JsonResponse({
            'status': 'success',
            'karma': post.get_karma(),
            'liked': liked,
            'disliked': disliked
        })

# Esta view já estava correta com @login_required.
@login_required
@permission_required('feedback.delete_feedback', raise_exception=True)
def null_feedback(request):
    post_id = request.POST.get('post_id')
    user = request.user
    feedback = get_object_or_404(Feedback, post_id=post_id, user=user)
    
    feedback.delete()

    post = get_object_or_404(Post, id=post_id)

    post.likes_count = post.feedback_posts.filter(feedback=True).count()
    post.dislikes_count = post.feedback_posts.filter(feedback=False).count()
    
    post.save()

    return JsonResponse({
        'status': 'success',
        'karma': post.get_karma(),
    })

# Apenas usuários com permissão para 'ver feedback' podem acessar esta lista.
@login_required
@permission_required('feedback.view_feedback', raise_exception=True)
def list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/list.html', {'feedbacks':feedbacks})