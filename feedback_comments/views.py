from django.shortcuts import redirect, get_object_or_404, render
from .models import Comment, FeedbackComment

def feedback(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        feedback = request.POST.get('feedback')
        user = request.user

        comment = get_object_or_404(Comment, id=comment_id)

        feedback_bool = True if feedback == 'like' else False

        feedback, created = FeedbackComment.objects.update_or_create(
            user=user,
            comment=comment,
            defaults={'feedback': feedback_bool}
        )

        return redirect('/comment/list/')
    
def list(request):
    feedbacks = FeedbackComment.objects.all()
    return render(request, 'feedback_comment/list.html', {'feedbacks':feedbacks})