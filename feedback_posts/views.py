from django.shortcuts import redirect, get_object_or_404, render
from .models import Post, FeedbackPost

def feedback(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        feedback = request.POST.get('feedback')
        user = request.user

        post = get_object_or_404(Post, id=post_id)

        feedback_bool = True if feedback == 'like' else False

        feedback, created = FeedbackPost.objects.update_or_create(
            user=user,
            post=post,
            defaults={'feedback': feedback_bool}
        )

        return redirect('/post/feedback/list/')
    
def null_feedback(request):
    post_id = request.POST.get('post_id')
    feedback_post = FeedbackPost.objects.get(post_id = post_id, user_id = request.user.id)
    feedback_post.delete()

    return redirect('/post/feedback/list/')
    

def list(request):
    feedbacks = FeedbackPost.objects.all()
    return render(request, 'feedback_post/list.html', {'feedbacks':feedbacks})