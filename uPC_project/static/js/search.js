function search(query) {
    // 로딩 이미지를 보여줌
    var loadingImg = document.createElement('img');
    loadingImg.src = '/static/img/aaa.gif';
    loadingImg.alt = 'Loading...';
    loadingImg.className = 'loading-image';

    // 로딩 이미지를 검색 폼의 자식으로 추가
    var searchForm = document.querySelector('.search');
    searchForm.appendChild(loadingImg);

    // 검색 결과 페이지로 이동
    window.location.href = '/search/?query=' + query;
}

// 검색 버튼 클릭 시 search 함수 실행
document.getElementById('into-search').addEventListener('click', function(event) {
    event.preventDefault(); // 기본 동작 방지
    var query = document.getElementsByName('query')[0].value;
    search(query);
});


