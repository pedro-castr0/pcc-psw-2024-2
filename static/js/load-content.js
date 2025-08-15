document.addEventListener('click', function(e) {

if (e.target.closest('.load-content')) {
    e.preventDefault();
    let link = e.target.closest('.load-content');
    let url = link.getAttribute('href');
    let target = document.querySelector(link.dataset.target);

    fetch(url)
        .then(res => res.text())
        .then(html => {
            target.innerHTML = html;
        });
    }
});

document.addEventListener("DOMContentLoaded", function(){
    document.getElementById('postButton').click()
})