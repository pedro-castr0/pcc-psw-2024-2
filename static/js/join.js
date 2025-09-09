function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = getCookie('csrftoken');

    document.querySelectorAll('button.btn-join').forEach(button => {
        button.addEventListener('click', function () {
            const btn = this;
            const communityId = btn.dataset.communityId;
            const isJoined = btn.dataset.joined === "true";
            const url = isJoined ? btn.dataset.leaveUrl : btn.dataset.joinUrl;

            const formData = new FormData();
            formData.append('community_id', communityId);

            fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken, 'Cache-Control': 'no-store' },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    btn.dataset.joined = data.joined;
                    document.getElementById(`join-text-${communityId}`).innerText = data.joined ? "Leave" : "Join";

                    btn.classList.toggle('button-white', !data.joined);
                    btn.classList.toggle('button-magenta', data.joined);

                    const countElem = document.getElementById(`members-count-${communityId}`);
                    if (countElem) countElem.innerText = data.members_count;
                } else {
                    console.error('Error join/leave');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
