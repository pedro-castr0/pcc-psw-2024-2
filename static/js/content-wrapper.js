document.addEventListener("DOMContentLoaded", function() {
    const POST_HEIGHT_LIMIT = 200;

    const wrappers = document.querySelectorAll(".post-content-wrapper");

    wrappers.forEach(wrapper => {
        const content = wrapper.querySelector(".post-content");
        const fade = wrapper.querySelector(".fade-overlay");
        const btn = wrapper.querySelector(".see-more-btn");

        if (content.scrollHeight > POST_HEIGHT_LIMIT) {
            fade.classList.remove("d-none");
            btn.classList.remove("d-none");
        } else {
            fade.classList.add("d-none");
            btn.classList.add("d-none");
        }
    });
});
