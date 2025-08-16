// JS
document.addEventListener('DOMContentLoaded', function() {
    const bell = document.getElementById('notification-bell');
    if (!bell) return;

    const url = bell.dataset.url; // pega a URL correta
    const countEl = document.getElementById('notification-count');
    const listEl = document.getElementById('notification-list');

    bell.addEventListener('click', function(e) {
        e.preventDefault();

        fetch(url)
            .then(res => res.json())
            .then(data => {
                // Atualiza contagem
                countEl.textContent = data.count;

                // Monta notificações
                let html = '';
                data.notifications.forEach(n => {
                    html += `
                        <li class="d-flex align-items-start mb-2">
                            <div class="col-md-2 col-sm-2 col-xs-2">
                                <div class="notify-img">
                                    <img src="${n.user_image}" alt="notification user image" class="rounded-circle" width="40">
                                </div>
                            </div>
                            <div class="col-md-10 col-sm-10 col-xs-10 flex-grow-1">
                                <a href="${n.link}" class="notification-user fw-bold text-dark">${n.user_name}</a>
                                <span class="notification-type text-muted">${n.message}</span>
                                <a href="${n.link}" class="notify-right-icon">
                                    <i class='bx bx-radio-circle-marked'></i>
                                </a>
                                <p class="time text-end">
                                    <span class="badge badge-pill badge-primary"><i class='${n.type_icon}'></i></span> ${n.time}
                                </p>
                            </div>
                        </li>
                    `;
                });

                listEl.innerHTML = html;
            })
            .catch(err => console.error('Erro ao carregar notificações:', err));
    });
});
