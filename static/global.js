document.getElementById('postForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value || 'Anonymous';
    const content = document.getElementById('content').value;
    const imageFile = document.getElementById('image').files[0];

    const formData = new FormData();
    formData.append('username', username);
    formData.append('content', content);
    if (imageFile) {
        formData.append('image', imageFile);
    }

    fetch('/post', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const postsDiv = document.getElementById('posts');
            const newPost = document.createElement('div');
            newPost.classList.add('post');

            let imageHtml = '';
            if (data.imageUrl) {
                imageHtml = `<img src="${data.imageUrl}" alt="Image" class="post-image">`;
            }

            const date = new Date(data.timestamp);
            const formattedDate = date.toLocaleString('pt-BR', { timeZone: 'UTC' });

            newPost.innerHTML = `<strong>${data.username}</strong>: ${data.content} <br><small>${formattedDate} | No.${data.id}</small>${imageHtml}`;
            postsDiv.prepend(newPost);
            document.getElementById('postForm').reset();
        });
});

// Carregar posts ao inicializar
function loadPosts() {
    fetch('/posts')
        .then(response => response.json())
        .then(posts => {
            const postsDiv = document.getElementById('posts');
            posts.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.classList.add('post');

                let imageHtml = '';
                if (post.imageUrl) {
                    imageHtml = `<img src="${post.imageUrl}" alt="Image" class="post-image">`;
                }

                const date = new Date(post.timestamp);
                const formattedDate = date.toLocaleString('pt-BR', { timeZone: 'UTC' });

                postDiv.innerHTML = `<strong>${post.username}</strong>: ${post.content} <br><small>${formattedDate} | No.${post.id}</small>${imageHtml}`;
                postsDiv.appendChild(postDiv);
            });
        });
}

// Carregar posts ao inicializar
loadPosts();