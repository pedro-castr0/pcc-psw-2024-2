document.addEventListener('DOMContentLoaded', function () {
    const csrfTokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (!csrfTokenElement) {
        console.error('CSRF token não encontrado na página.');
        return;
    }
    const csrfToken = csrfTokenElement.value;

    document.body.addEventListener('click', function (e) {
        const btn = e.target.closest('button[data-feedback]');
        if (!btn) return;

        const postId = btn.dataset.postId;
        const feedback = btn.dataset.feedback;

        let isActive = false;
        if (feedback === 'like') {
            isActive = btn.dataset.positiveFeedback === "true";
        } else if (feedback === 'dislike') {
            isActive = btn.dataset.negativeFeedback === "true";
        }

        const url = isActive ? btn.dataset.urlNull : btn.dataset.urlFeedback;

        const formData = new FormData();
        formData.append('post_id', postId);
        formData.append('feedback', feedback);

        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken, 'Cache-Control': 'no-store' },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const likeCountElem = document.getElementById(`like-count-${postId}`);
            const dislikeCountElem = document.getElementById(`dislike-count-${postId}`);
            if (likeCountElem) likeCountElem.innerText = data.likes_count;
            if (dislikeCountElem) dislikeCountElem.innerText = data.dislikes_count;

            const likeBtn = document.getElementById(`like-btn-${postId}`);
            const dislikeBtn = document.getElementById(`dislike-btn-${postId}`);

            if (feedback === 'like') {
                likeBtn.querySelector('i').classList.toggle('text-success', data.liked);
                likeBtn.querySelector('i').classList.toggle('text-dark', !data.liked);
                likeBtn.dataset.positiveFeedback = data.liked;

                if (dislikeBtn) {
                    dislikeBtn.querySelector('i').classList.remove('text-danger');
                    dislikeBtn.querySelector('i').classList.add('text-dark');
                    dislikeBtn.dataset.negativeFeedback = "false";
                }
            } else if (feedback === 'dislike') {
                dislikeBtn.querySelector('i').classList.toggle('text-danger', data.disliked);
                dislikeBtn.querySelector('i').classList.toggle('text-dark', !data.disliked);
                dislikeBtn.dataset.negativeFeedback = data.disliked;

                if (likeBtn) {
                    likeBtn.querySelector('i').classList.remove('text-success');
                    likeBtn.querySelector('i').classList.add('text-dark');
                    likeBtn.dataset.positiveFeedback = "false";
                }
            }
        })
        .catch(error => console.error('Erro ao enviar feedback:', error));
    });
});
