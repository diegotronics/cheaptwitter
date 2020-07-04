document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault()
            let post_id = this.id;
            let content = document.getElementById('content-' + post_id);

            let form = document.createElement("form");
            form.id = 'form-' + post_id;

            let input_id = document.createElement("input");
            input_id.classList.add('d-none');
            input_id.setAttribute('name', 'post_id');
            input_id.value = post_id;

            let textarea = document.createElement("textarea");
            textarea.setAttribute('name', 'content');
            textarea.setAttribute('rows', '3');
            textarea.classList.add('form-control')
            textarea.value = content.innerHTML;

            let save = document.createElement("button");
            save.setAttribute('type', 'submit');
            save.classList.add('btn');
            save.classList.add('btn-primary');
            save.classList.add('my-2');
            save.id = 'save-' + post_id;
            save.innerHTML = "Save";

            form.insertAdjacentHTML('afterbegin', csrftoken)
            form.appendChild(textarea)
            form.appendChild(input_id)
            form.appendChild(save)

            content.innerHTML = "";
            content.appendChild(form);

            document.getElementById('save-' + post_id).addEventListener('click', function (e) {
                e.preventDefault()
                const request = new XMLHttpRequest();

                request.open('POST', '/edit_post');
                request.onload = () => {
                    if (request.status == 200) {
                        window.location.reload();
                    }
                }
                let formdata = document.getElementById('form-' + post_id);
                formdata = new FormData(formdata);

                request.send(formdata);
            });
        });
    });
    document.querySelectorAll('.like').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            let post_id = this.children[0].id.split('-');
            post_id = post_id[1];
            data = new FormData();
            data.append('post_id', post_id)
            fetch('/likes', {
                    method: 'POST',
                    body: data,
                })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    let liked = document.getElementById('liked-' + post_id);
                    let count = document.getElementById('count-' + post_id);
                    count.innerHTML = result.count
                    if (result.liked) {
                        liked.classList.remove('text-dark');
                        liked.classList.add('text-danger');
                    } else {
                        liked.classList.remove('text-danger');
                        liked.classList.add('text-dark');
                    }

                });
        });
    });
});