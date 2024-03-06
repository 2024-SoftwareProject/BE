# BE
2024 소프트웨어프로젝트 준비

**clone 할때 DB, migrations files 다 삭제하고 create DB, migation 진행해야함**
**그리고 private setting file 자기 db에 맞게 설정 변경**

~2/13
가상환경, django, gitignore, mysql 세팅
signup(회원가입)로직 구현 (로그인 자체 코드는 금방할 것 같은데 회원 관리 db부터 막힘...)

*DB문제
mysql 설치해서 uPC용 db까지는 어찌저찌 설치했다만,, 테이블 어케 관리하는겨..어휴
연결도 맞게 했는지 모르겠고
pc db서버에 연결해뒀는데(localhost) pc를 항상 켤 수는 없으니,, 노트북에 연결해야하나 고민,,
아니 이걸 원격에 할 수는 없나?

*라이브러리(?) 문제
django.core.exceptions.ImproperlyConfigured: WSGI application 'uPC.wsgi.application' could not be loaded; Error importing module.
어떤 블로거가 로그인 구현할 때 어떤 패키지 깔길래 나도 해봤는데 망,,, 여기부터 뇌 안 돌아감..

*gitignore문제
이것도 db문제랑 연결되는데 db password를 감춰야 해서 gitignore 하면 import private_settings 가 안 되는 문제,,

==============

~2/26
accounts구현
회원가입 // 닉네임, 비밀번호 2중확인
로그인 // 닉네임, 비밀번호
로그아웃
회원삭제
마이페이지
프로필업데이트 // 메일, 이름 수정가능

++ html상속관계 리드코드 작성

+++ 카카오 api 연동시도했지만 html에 나타나지 않음
우선, backend에서 할 수 있는 영역은 아님
front에서 담당 요망


===========

~2/29
accounts 수정 및 html 리드 코드 작성
로그인
로그아웃
회원탈퇴
회원정보 수정
비밀번호 변경
마이페이지
