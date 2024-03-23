function search(query) {

    var darkBackground = document.createElement('div');
    darkBackground.style.position = 'fixed';
    darkBackground.style.top = '0';
    darkBackground.style.left = '0';
    darkBackground.style.width = '100%';
    darkBackground.style.height = '100%';
    darkBackground.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'; // 투명도가 0.5인 검은색 배경
    darkBackground.style.zIndex = '9999'; // .gif보다 위에 배치되도록 z-index를 설정
    document.body.appendChild(darkBackground);


    var loadingImg = document.createElement('img');
    loadingImg.src = '/static/img/load.gif';
    loadingImg.alt = 'Loading...';
    loadingImg.className = 'loading-image';
    loadingImg.style.position = 'fixed';
    loadingImg.style.top = '50%';
    loadingImg.style.left = '50%';
    loadingImg.style.transform = 'translate(-50%, -50%)';
    loadingImg.style.zIndex = '10000';
    
    document.body.appendChild(loadingImg);

    // 검색 결과 페이지로 이동
    window.location.href = '/search/?query=' + query;
}

// 검색 버튼 클릭 시 search 함수 실행
document.getElementById('updateModal').addEventListener('click', function(event) {
    var query = document.getElementsByName('query')[0].value;
    search(query);
});