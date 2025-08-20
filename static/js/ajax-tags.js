document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('tag-input');
    const dropdown = document.getElementById('autocomplete-dropdown');
    const template = document.getElementById('tag-suggestions');
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
                if (!data || data.length === 0) {
                    const li = document.createElement('li');
                    li.className = 'dropdown-item text-muted';
                    li.textContent = 'Nenhuma tag encontrada';
                    dropdown.appendChild(li);
                } else {
                    data.forEach(tag => {
                        const clone = template.content.cloneNode(true);
                        const li = clone.querySelector('.dropdown-item');

                        const startIdx = tag.toLowerCase().indexOf(query.toLowerCase());
                        if (startIdx !== -1) {
                            li.innerHTML = tag.substring(0, startIdx) +
                                           '<strong>' + tag.substring(startIdx, startIdx + query.length) + '</strong>' +
                                           tag.substring(startIdx + query.length);
                        } else {
                            li.textContent = tag;
                        }

                        li.addEventListener('click', () => {
                            input.value = tag;
                            dropdown.style.display = 'none';
                        });

                        dropdown.appendChild(clone);
                    });
                }

                dropdown.style.display = 'block';
            })
            .catch(err => console.error('Erro ao carregar tags:', err));
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
