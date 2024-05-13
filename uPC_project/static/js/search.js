function search(query) {
    var query = get_url_parameter('query');
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
document.getElementById('yes-btn').addEventListener('click', function(event) {
    // 이 곳에 예 버튼이 눌렸을 때 실행할 동작을 작성하세요.
    // 예를 눌렀을 때 모달이 닫히도록 할 수 있습니다.
    search(query); // update 함수를 호출하는 예시입니다.
});