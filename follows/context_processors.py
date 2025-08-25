def following(request):
    if request.user.is_authenticated:
        following_ids = set(
            request.user.following.values_list('followed_id', flat=True)
        )

    else:
        following_ids = set()

    return {
        'following_ids': following_ids,
    }
