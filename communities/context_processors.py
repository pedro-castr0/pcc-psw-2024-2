def owned(request):
    if request.user.is_authenticated:
        owned_communities_ids = set(
            request.user.communities.values_list('id', flat=True)
        )

    else:
        owned_communities_ids = set()

    return {
        'owned_communities_ids': owned_communities_ids,
    }
