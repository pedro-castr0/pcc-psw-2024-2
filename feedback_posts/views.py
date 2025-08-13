from django.shortcuts import redirect, get_object_or_404, render
from .models import Post, FeedbackPost
from django.http import JsonResponse

def feedback(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        feedback_type = request.POST.get('feedback')  # 'like' ou 'dislike'
        user = request.user

        post = get_object_or_404(Post, id=post_id)

        is_like = True if feedback_type == 'like' else False

        fb_obj, created = FeedbackPost.objects.update_or_create(
            user=user,
            post=post,
            defaults={'feedback': is_like}
        )

        post.likes_count = post.feedback_posts.filter(feedback=True).count()
        post.dislikes_count = post.feedback_posts.filter(feedback=False).count()
        post.save()

        liked = post.feedback_posts.filter(user=user, feedback=True).exists()
        disliked = post.feedback_posts.filter(user=user, feedback=False).exists()

        return JsonResponse({'status': 'success', 'created': created, 'likes_count': post.likes_count, 'dislikes_count': post.dislikes_count, 'liked': liked, 'disliked': disliked})
    
def null_feedback(request):
    post_id = request.POST.get('post_id')
    user = request.user
    feedback_post = get_object_or_404(FeedbackPost, post_id=post_id, user=user)
    
    feedback_post.delete()

    post = get_object_or_404(Post, id=post_id)

    post.likes_count = post.feedback_posts.filter(feedback=True).count()
    post.dislikes_count = post.feedback_posts.filter(feedback=False).count()
    
    post.save()

    return JsonResponse({'status': 'success', 'likes_count': post.likes_count, 'dislikes_count': post.dislikes_count})

def list(request):
    feedbacks = FeedbackPost.objects.all()
    return render(request, 'feedback_post/list.html', {'feedbacks':feedbacks})