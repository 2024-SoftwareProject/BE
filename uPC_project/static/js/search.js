function search(query) {
    // 로딩 이미지를 보여줌
    var loadingImg = document.createElement('img');
    loadingImg.src = '/static/img/aaa.gif';
    loadingImg.alt = 'Loading...';
    loadingImg.className = 'loading-image';
    document.body.appendChild(loadingImg);

    // 검색 결과 페이지로 이동
    window.location.href = '/search/?query=' + query;
}

// 검색 버튼 클릭 시 search 함수 실행
document.getElementById('gogo').addEventListener('click', function() {
    var query = document.getElementsByName('query')[0].value;
    search(query);
});


