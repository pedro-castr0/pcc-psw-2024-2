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

        // Verifica se o botão já está ativo
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
            const karmaElem = document.getElementById(`karma-${postId}`);

            let k = Number(data?.karma) || 0;
            if (karmaElem) {
                karmaElem.textContent = k > 0 ? `+${k}` : String(k);
                karmaElem.classList.remove('text-green', 'text-red', 'text-blurred');
                if (k > 0) karmaElem.classList.add('text-green');
                else if (k < 0) karmaElem.classList.add('text-red');
                else karmaElem.classList.add('text-blurred');
            }

            const likeBtn = document.getElementById(`like-btn-${postId}`);
            const dislikeBtn = document.getElementById(`dislike-btn-${postId}`);

            if (!data.liked && !data.disliked) {
                if (likeBtn) {
                    likeBtn.querySelector('i').classList.remove('text-green');
                    likeBtn.querySelector('i').classList.add('text-blurred');
                    likeBtn.dataset.positiveFeedback = "false"; // reset
                }
                if (dislikeBtn) {
                    dislikeBtn.querySelector('i').classList.remove('text-red');
                    dislikeBtn.querySelector('i').classList.add('text-blurred');
                    dislikeBtn.dataset.negativeFeedback = "false"; // reset
                }
                return;
            }

            if (data.liked) {
                if (likeBtn) {
                    likeBtn.querySelector('i').classList.add('text-green');
                    likeBtn.querySelector('i').classList.remove('text-blurred');
                    likeBtn.dataset.positiveFeedback = "true";
                }
                if (dislikeBtn) {
                    dislikeBtn.querySelector('i').classList.remove('text-red');
                    dislikeBtn.querySelector('i').classList.add('text-blurred');
                    dislikeBtn.dataset.negativeFeedback = "false";
                }
            }

            if (data.disliked) {
                if (dislikeBtn) {
                    dislikeBtn.querySelector('i').classList.add('text-red');
                    dislikeBtn.querySelector('i').classList.remove('text-blurred');
                    dislikeBtn.dataset.negativeFeedback = "true";
                }
                if (likeBtn) {
                    likeBtn.querySelector('i').classList.remove('text-green');
                    likeBtn.querySelector('i').classList.add('text-blurred');
                    likeBtn.dataset.positiveFeedback = "false";
                }
            }
        })
        .catch(error => console.error('Erro ao enviar feedback:', error));
    });
});
