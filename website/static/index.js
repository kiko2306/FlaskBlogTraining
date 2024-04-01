function like(postId){
    const likeCount = document.getElementById('likes-count-$(postId)');
    const likeButton = document.getElementById('likes-button-$(postId)');

    fetch('/like_post/${postId}',{method:"POST"})
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data["likes"];
    });

}