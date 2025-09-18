document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('search-input');
    const dropdown = document.getElementById('search-dropdown');
    const template = document.getElementById('search-suggestions');
    const autocompleteUrl = input.closest('form').dataset.autocompleteUrl;

    let currentFocus = -1;

    input.addEventListener('input', function() {
        const query = input.value.trim();
        dropdown.innerHTML = '';
        currentFocus = -1;

        if (!query) {
            dropdown.style.display = 'none';
            return;
        }

        fetch(`${autocompleteUrl}?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                let results = [];

                // junta todas as listas do JSON em uma só
                if (data.users) results = results.concat(data.users);
                if (data.communities) results = results.concat(data.communities);
                if (data.posts) results = results.concat(data.posts);

                if (!results || results.length === 0) {
                    const li = document.createElement('li');
                    li.className = 'dropdown-item text-muted';
                    li.textContent = 'Nenhum resultado encontrado';
                    dropdown.appendChild(li);
                } else {
                    results.forEach(result => {
                        const clone = template.content.cloneNode(true);
                        const li = clone.querySelector('.dropdown-item');

                        const startIdx = result.toLowerCase().indexOf(query.toLowerCase());
                        if (startIdx !== -1) {
                            li.innerHTML = result.substring(0, startIdx) +
                                           '<strong>' + result.substring(startIdx, startIdx + query.length) + '</strong>' +
                                           result.substring(startIdx + query.length);
                        } else {
                            li.textContent = result;
                        }

                        li.addEventListener('click', () => {
                            input.value = result;
                            dropdown.style.display = 'none';
                        });

                        dropdown.appendChild(clone);
                    });
                }

                dropdown.style.display = 'block';
            })
            .catch(err => console.error('Erro ao carregar sugestões:', err));
    });

    // Navegação com teclado
    input.addEventListener('keydown', function(e) {
        const items = dropdown.querySelectorAll('.dropdown-item');
        if (!items) return;

        if (e.key === "ArrowDown") {
            currentFocus++;
            addActive(items);
        } else if (e.key === "ArrowUp") {
            currentFocus--;
            addActive(items);
        } else if (e.key === "Enter") {
            e.preventDefault();
            if (currentFocus > -1 && items[currentFocus]) {
                items[currentFocus].click();
            }
        }
    });

    function addActive(items) {
        removeActive(items);
        if (currentFocus >= items.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = items.length - 1;
        items[currentFocus].classList.add('active');
    }

    function removeActive(items) {
        items.forEach(item => item.classList.remove('active'));
    }

    // Fecha ao clicar fora
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
});
