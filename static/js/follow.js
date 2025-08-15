document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-follow').forEach(button => {
        button.addEventListener('click', function() {
            const btn = this;
            const userId = btn.dataset.userId;
            const isFollowing = btn.dataset.following === "true";

            const url = isFollowing ? UNFOLLOW_URL : FOLLOW_URL;

            const formData = new FormData();
            formData.append('followed_id', userId);

            fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': CSRF_TOKEN, 'Cache-Control': 'no-store' },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Atualiza estado do botão
                    btn.dataset.following = data.following;

                    // Atualiza texto do botão
                    const textElem = btn.querySelector('.follow-text');
                    if (textElem) textElem.innerText = data.following ? "Unfollow" : "Follow";

                    // Atualiza classes do botão
                    if (data.following) {
                        btn.classList.remove('btn-primary');
                        btn.classList.add('btn-danger');
                    } else {
                        btn.classList.remove('btn-danger');
                        btn.classList.add('btn-primary');
                    }

                    // Atualiza contagem de followers em todos os spans correspondentes
                    document.querySelectorAll(`.followers-count[data-user-id="${userId}"]`).forEach(span => {
                        span.innerText = data.followers_count;
                    });
                } else {
                    console.error(data.message || 'Erro ao seguir/desseguir');
                }
            })
            .catch(error => console.error('Erro no follow/unfollow:', error));
        });
    });
});
