function toggleReplyForm(id) {
    const form = document.getElementById(`reply-form-${id}`);
    form.classList.toggle("d-none");
}

function toggleReplies(commentId) {
    let container = document.getElementById("replies-" + commentId);
    let btnText = document.getElementById("btn-text-" + commentId);

    if (container) {
        container.classList.toggle("d-none");
        if (container.classList.contains("d-none")) {
            btnText.textContent = "Show replies";
        } else {
            btnText.textContent = "Hide replies";
        }
    }
}


