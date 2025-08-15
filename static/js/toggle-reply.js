function toggleReplyForm(id) {
    const form = document.getElementById(`reply-form-${id}`);
    form.classList.toggle("d-none");
}

function toggleReplies(commentId) {
    let container = document.getElementById("replies-" + commentId);
    if (container.classList.contains("d-none")) {
        container.classList.remove("d-none");
    } else {
        container.classList.add("d-none");
    }
}