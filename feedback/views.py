from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Post, Feedback
from django.http import JsonResponse

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
    
@login_required
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

@login_required
def list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/list.html', {'feedbacks':feedbacks})