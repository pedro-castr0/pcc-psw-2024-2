document.addEventListener('DOMContentLoaded', function() {
    const input = document.querySelector('.navbar-search input');
    const dropdown = document.createElement('div');
    dropdown.classList.add('tag-dropdown');
    dropdown.style.position = 'absolute';
    dropdown.style.background = 'white';
    dropdown.style.border = '1px solid #ccc';
    dropdown.style.zIndex = '1000';
    dropdown.style.maxHeight = '200px';
    dropdown.style.overflowY = 'auto';
    input.parentNode.appendChild(dropdown);

    let currentFocus = -1; // Para navegação com setas

    input.addEventListener('input', function() {
        const query = input.value;
        if (!query) {
            dropdown.innerHTML = '';
            return;
        }

        fetch(`/tags/autocomplete/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                dropdown.innerHTML = '';
                currentFocus = -1;

                data.forEach(tag => {
                    const div = document.createElement('div');
                    // Destacar a parte que bate com a pesquisa
                    const startIdx = tag.toLowerCase().indexOf(query.toLowerCase());
                    if (startIdx !== -1) {
                        div.innerHTML = tag.substring(0, startIdx) 
                                        + "<strong>" + tag.substring(startIdx, startIdx + query.length) + "</strong>" 
                                        + tag.substring(startIdx + query.length);
                    } else {
                        div.textContent = tag;
                    }
                    div.style.padding = '5px';
                    div.style.cursor = 'pointer';

                    div.addEventListener('click', () => {
                        input.value = tag; // completa o texto
                        dropdown.innerHTML = '';
                    });

                    dropdown.appendChild(div);
                });
            });
    });

    // Navegação com setas e Enter
    input.addEventListener("keydown", function(e) {
        let items = dropdown.getElementsByTagName("div");
        if (!items) return;

        if (e.key === "ArrowDown") {
            currentFocus++;
            addActive(items);
        } else if (e.key === "ArrowUp") {
            currentFocus--;
            addActive(items);
        } else if (e.key === "Enter") {
            e.preventDefault();
            if (currentFocus > -1) {
                if (items[currentFocus]) items[currentFocus].click();
            }
        }
    });

    function addActive(items) {
        if (!items) return false;
        removeActive(items);
        if (currentFocus >= items.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = items.length - 1;
        items[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(items) {
        for (let i = 0; i < items.length; i++) {
            items[i].classList.remove("autocomplete-active");
        }
    }

    // Fecha dropdown ao clicar fora
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target)) {
            dropdown.innerHTML = '';
        }
    });
});
