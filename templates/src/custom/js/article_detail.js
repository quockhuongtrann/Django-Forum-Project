const commentForm = document.forms.commentForm
const commentFormContent = commentForm.content
const commentFormParentInput = commentForm.parent
commentForm.addEventListener('submit', createComment)

replyUser()
deleteAll()



function deleteAll() {
    document.querySelectorAll('.btn-delete').forEach((e) => {
        e.addEventListener('submit', deleteComment)
    })
}

function deleteComment(event) {
    event.preventDefault()
    const commentArticleId = commentForm.getAttribute('data-article-id');
    console.log("commentArticleId", commentArticleId)
    const commentNestedListBox = document.querySelector('.nested-comments');
    fetch(`/articles/${commentArticleId}/comments/delete/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
        },
        body: null
    })
    .then((response => response.json()))
    .then((result) => {
        console.log(result['payload'])
    })
}

function replyUser() {
    document.querySelectorAll('.btn-reply').forEach((e) => {
    e.addEventListener('click', replyComment)
})
}

function replyComment() {
    const commentMessage = this;
    const commentUsername = commentMessage.getAttribute('data-comment-username');
    const commentMessageId = commentMessage.getAttribute('data-comment-id');
    commentFormContent.value = `**${commentUsername}**, `
    commentFormParentInput.value = `${commentMessageId}`
}

function createComment(event) {
    event.preventDefault()
    const commentFormSubmit = commentForm.commentSubmit;
    const commentArticleId = commentForm.getAttribute('data-article-id');
    const commentNestedListBox = document.querySelector('.nested-comments');

    commentFormSubmit.disabled = true;
    commentFormSubmit.innerText = "Đang chờ phản hồi";

    fetch(`/articles/${commentArticleId}/comments/create/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
        },
        body: new FormData(commentForm)
    }).then((response => response.json())).then((result) => {
        if (result['comment_is_child']) {
            const commentParentThreadList = document.querySelector(`#comment-thread-${result['comment_parent_id']}`);
            commentParentThreadList.innerHTML += `
               <ul id="comment-thread-${result['comment_id']}">
                    <li class="card border-0">
                        <div class="row">
                            <div class="col-md-2" >
                                <img src="${result['comment_avatar']}" class="rounded-circle" style="width: 120px;height: 120px;object-fit: cover;" alt="${result['comment_author']}"/>
                            </div>
                            <div class="col-md-10">
                                <div class="card-body">
                                    <h6 class="card-title">
                                        <a href="${result['comment_get_absolute_url']}">${result['comment_author']}</a>
                                    </h6>
                                    <p class="card-text">
                                        ${result['comment_content']}
                                    </p>
                                    <a class="btn btn-sm btn-dark btn-reply" href="#commentForm" data-comment-id="${result['comment_id']}" data-comment-username="${result['comment_author']}">Phản hồi</a>
                                    <form method="post" style="display: inline-block;">
                                        <div class="d-grid gap-2 d-md-block mt-2">
                                        <button type="submit" class="btn btn-sm btn-danger" href="#commentForm">Xoá</button>
                                        </div>
                                    </form>
                                    <hr/>
                                    <time>${result['comment_created_at']}</time>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            `
        } else {
            commentNestedListBox.innerHTML += `
            <ul id="comment-thread-${result['comment_id']}">
                    <li class="card border-0">
                        <div class="row">
                            <div class="col-md-2">
                                <img src="${result['comment_avatar']}" class="rounded-circle" style="width: 120px;height: 120px;object-fit: cover;" alt="${result['comment_author']}"/>
                            </div>
                            <div class="col-md-10">
                                <div class="card-body">
                                    <h6 class="card-title">
                                        <a href="${result['comment_get_absolute_url']}">${result['comment_author']}</a>
                                    </h6>
                                    <p class="card-text">
                                        ${result['comment_content']}
                                    </p>
                                    <a class="btn btn-sm btn-dark btn-reply" href="#commentForm" data-comment-id="${result['comment_id']}" data-comment-username="${result['comment_author']}">Phản hồi</a>
                                    <form method="post" style="display: inline-block;">
                                        <div class="d-grid gap-2 d-md-block mt-2">
                                        <button type="submit" class="btn btn-sm btn-danger" href="#commentForm">Xoá</button>
                                        </div>
                                    </form>
                                    <hr/>
                                    <time>${result['comment_created_at']}</time>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            `
        }
        commentForm.reset()
        commentFormSubmit.disabled = false;
        commentFormSubmit.innerText = "Thêm";
        commentFormParentInput.value = null;
        replyUser()
    })
}