## ***u.PC 프로젝트***

**중고 컴퓨터 부품 통합 검색 서비스**

<img src="https://github.com/2024-SoftwareProject/BE/assets/127396481/a2fe1264-ad49-4134-bb93-0d051345f79c" width="20%" height="20%">

user-platform-computer의 약어로,

"사용자와 컴퓨터를 연결시켜주는 platform"이라는 의미를 담고 있다.



## [핵심 주요 기능]

1. 크롤링_<당근마켓, 번개장터, 중고나라 중고 제품 데이터> **(Selenium, beautifulSoup 활용)**

2. (사용자 검색 쿼리 기반/카테고리 기반) 제품 검색 엔진

3. 사용자 맞춤형 제품 추천 알고리즘 **(KNN 알고리즘-User Based Collaborative Filtering)**

4. 커뮤니티 


## [기타 기능]

1. 회원관리



## [서비스 효과]
1. 시간 절약

   3사 플랫폼 검색 데이터를 하나로 모아 사용자가 검색하는 데 들이는 시간을 단축시킨다.

2. 정보 획득

   커뮤니트 공간을 통해 전문성이 필요한 pc 관련 정보를 쉽게 얻을 수 있도록 한다.

3. 고민 해결

   사용자 맞춤형 추천 알고리즘으로 구매 결정에 도움을 준다.



## [개발 환경]

   language : python

   framework : django

   os : mac, window, linux

   database : mysql

   release : amazon ec2


## [라이브러리]

   크롤링 : selenium, beautifulSoup

   추천 알고리즘 : scikit-learn (KNN방식_User-Based Collaborative Filtering)

   디자인 : django_bootstrap5




## [코드 참조 시 유의 사항]

1. 설정 변경
   - private_settings.py
   ```py
   # Database
   # https://docs.djangoproject.com/en/5.0/ref/settings/#databases
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_dbName', # mydatabase
           'USER': 'root', # mydatabaseuser
           'PASSWORD': 'your_password', # mypassword
           'HOST': 'localhost', # host
           'PORT': '3306',
       }
   }
   
   # SECURITY WARNING: keep the secret key used in production secret!
   SECRET_KEY = 'your_secret_key'
   
   # Email smtp
   EMAIL_HOST_PASSWORD = 'your_email_password'
   # 사전에 stmp 연동 필요
   ```
   
   - accounts_app/helper.py
   ```py
   24행|send_mail(subject, recipient_list, body='', from_email='your_email', fail_silently=False, html=None, *args, **kwargs)
   ```

3. 서비스 도메인 변경

   accounts_app/templates/accounts/signup_email.html

   이메일 인증 후 리다이렉트 주소 목적에 맞게 수정
   ```html
   # 로컬에서 테스트 실행 시 다음으로 설정
   12행 | http://127.0.0.0:8000
   ```

4. 추천알고리즘_사전에 유저 생성
   ```py
   # 관리자 유저 생성
   python manage.py createsuperuser
   ```
   recommend_app/recommendations.py
   
   model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=2, n_jobs=-1)의
   n_neightbors크기에 맞춰 유저 생성 필요

5. 데이터베이스 migrate
   모델 상속 관계에 의해 데이터베이스 충돌 시 다음 순서로 makemigrations/migrate 진행
   ```shell
   python manage.py migrate category_app
   python manage.py migrate products_app
   python manage.py migrate accounts_app
   python manage.py migrate board_app
   python manage.py migrate
   ```
