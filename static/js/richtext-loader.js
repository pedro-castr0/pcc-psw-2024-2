document.addEventListener('DOMContentLoaded', function () {
    const quill = new Quill('#rich-text-loader', {
        theme: 'snow',
        placeholder: 'Write something...',
        modules: {
            toolbar: [
                [
                    {'font': []},
                    {'header': []},
                    {'align': []},
                    'bold', 'italic', 'underline', 'strike', 'blockquote',
                    {'color': []},
                    {'background': []},
                ],
                ['code-block', 'link'],
                ['clean'],
                ['image'],
                ['video']
            ]
        },
        class:"rounded border"
    });

    quill.getModule('toolbar').container.classList.add(
        'rounded', 'border'
    );

    quill.clipboard.addMatcher('img', function(node, delta) {
        node.setAttribute(
            'style',
            'max-width:400px; height:auto; border-radius:12px; border:3px solid #4CAF50; margin-top:15px;'
        );
        return delta;
    });

    const form = document.getElementById('rich-text-form');
    const hidden = form.querySelector('#container');

    function sync() { hidden.value = quill.root.innerHTML; }
    quill.on('text-change', sync);
    sync();
    form.addEventListener('submit', sync);

});