document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".comment-box").forEach(box => {
        const textarea = box.querySelector("textarea");
        const actions = box.querySelector(".comment-actions");
        const cancelBtn = box.querySelector(".btn-cancel");

        const originalHeight = textarea.style.height || "";

        textarea.addEventListener("focus", () => {
            actions.classList.remove("d-none");
            textarea.style.height = "100px";
        });

        cancelBtn.addEventListener("click", () => {
            textarea.value = "";
            actions.classList.add("d-none");
            textarea.style.height = originalHeight;
        });
    });
});
