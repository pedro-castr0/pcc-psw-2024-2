def joined(request):
    if request.user.is_authenticated:
        community_ids = set(
            request.user.joined_communities.values_list('community_id', flat=True)
        )

    else:
        community_ids = set()

    return {
        'community_ids': community_ids
    }