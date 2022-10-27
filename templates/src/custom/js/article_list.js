ratingAll()

function ratingAll() {
    document.querySelectorAll('.btn-like, .btn-dislike').forEach((e) => {
    e.addEventListener('click', createRating)
})
}

function createRating(event) {
    event.preventDefault()
    const rating = this;
    const ratingId = rating.getAttribute('data-id');
    const ratingAction = rating.getAttribute('data-action');
    const likeSum =  document.querySelector(`button[data-rating-like='${ratingId}']`);
    const dislikeSum =  document.querySelector(`button[data-rating-dislike='${ratingId}']`);
    const authorStatus =  document.querySelector(`a[author-rating-status='${ratingId}']`);
    fetch(`/articles/${ratingId}/${ratingAction}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
        },
    }).then((response) => response.json()).then((result) => {
                if (result['error']) {
                    console.log(result['error'])
                } else {
                    likeSum.innerHTML = `Like (${result['get_like_sum']})`
                    dislikeSum.innerHTML = `Dislike (${result['get_dislike_sum']})`
                    authorStatus.innerHTML = `${result['status']}`
                }
        })
}