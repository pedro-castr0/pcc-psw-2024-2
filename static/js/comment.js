document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.comment-form, .reply-form').forEach(form => {
        form.addEventListener('submit', e => {
            e.preventDefault();

            const postId = form.dataset.postId;
            const parentId = form.dataset.commentId || null;
            const content = form.querySelector('textarea').value;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch("{% url 'comment' %}", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    post: postId,
                    content: content,
                    parent: parentId
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    if (!data.parent_id) {
                        // comentário principal
                        document.getElementById(`comments-area-${postId}`)
                                .insertAdjacentHTML('afterbegin', data.comment_html);
                    } else {
                        // resposta
                        document.getElementById(`replies-${data.parent_id}`)
                                .insertAdjacentHTML('beforeend', data.comment_html);
                    }
                    form.reset();
                    const counter = document.getElementById(`comments-count-${postId}`);
                    if (counter) counter.innerText = data.comments_count;
                }
            });
        });
    });
});
