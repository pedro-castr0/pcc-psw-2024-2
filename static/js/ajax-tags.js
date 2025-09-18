document.addEventListener("DOMContentLoaded", function () {
    const tagsDropdown = document.getElementById("tags-dropdown");
    const form = document.querySelector("form.navbar-search");
    const tagsUrl = form.dataset.tagsUrl;

    fetch(tagsUrl)
        .then(response => response.json())
        .then(data => {
            tagsDropdown.innerHTML = ""; // limpa "Carregando tags..."

            if (data.length === 0) {
                tagsDropdown.innerHTML = `<li class="dropdown-item text-muted">Nenhuma tag encontrada</li>`;
                return;
            }

            data.forEach(tag => {
                const li = document.createElement("li");
                li.classList.add("dropdown-item");

                li.innerHTML = `
                    <div class="form-check">
                        <input class="form-check-input tag-checkbox" type="checkbox" 
                               value="${tag.id}" id="tag-${tag.id}" name="tags">
                        <label class="form-check-label" for="tag-${tag.id}">
                            ${tag.name}
                        </label>
                    </div>
                `;

                tagsDropdown.appendChild(li);
            });
        })
        .catch(error => {
            console.error("Erro ao carregar tags:", error);
            tagsDropdown.innerHTML = `<li class="dropdown-item text-danger">Erro ao carregar tags</li>`;
        });
});
