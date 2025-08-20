document.addEventListener('DOMContentLoaded', function() {
    const bell = document.getElementById('notification-bell');
    if (!bell) return;

    const url = bell.dataset.url;
    const countEl = document.getElementById('notification-count');
    const countTitleEl = document.getElementById('notification-count-title');
    const listEl = document.getElementById('notification-list');
    const template = document.getElementById('notification-template');

    bell.addEventListener('click', function(e) {
        e.preventDefault();

        fetch(url)
            .then(res => res.json())
            .then(data => {
                countEl.textContent = data.count;
                countTitleEl.textContent = data.count;

                // Limpa lista
                listEl.innerHTML = '';

                if (data.notifications.length === 0) {
                    listEl.innerHTML = '<li class="text-center text-muted">Nenhuma notificação</li>';
                    return;
                }

                data.notifications.forEach(n => {
                    // Clona o template
                    const clone = template.content.cloneNode(true);
                    clone.querySelector('img').src = n.user_image;
                    clone.querySelector('img').alt = `${n.user_name} image`;
                    clone.querySelector('.notification-user').href = n.link;
                    clone.querySelector('.notification-user').textContent = n.user_name;
                    clone.querySelector('.notification-type').textContent = n.message;
                    clone.querySelector('i').className = n.type_icon;
                    clone.querySelector('.notification-time').textContent = n.time;

                    listEl.appendChild(clone);
                });
            })
            .catch(err => console.error('Erro ao carregar notificações:', err));
    });
});
