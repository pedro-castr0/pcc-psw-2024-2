def feedbacks(request):
    if request.user.is_authenticated:
        positive_feedbacks = set(
            request.user.feedbacks.filter(feedback=True).values_list('post_id', flat=True)
        )

        negative_feedbacks = set(
            request.user.feedbacks.filter(feedback=False).values_list('post_id', flat=True)
        )

    else:
        positive_feedbacks = set()
        negative_feedbacks = set()

    return {
        'positive_feedbacks': positive_feedbacks, 'negative_feedbacks': negative_feedbacks
    }