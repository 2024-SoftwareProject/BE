**UPC 프로젝트**


===============
[코드 참고 시 유의 사항]
1. private_settings.py 설정 변경
```py
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb', # mydatabase
        'USER': 'root', # mydatabaseuser
        'PASSWORD': 'password', # mypassword
        'HOST': 'localhost', # host
        'PORT': '3306',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your secret_key'

# Email smtp
EMAIL_HOST_PASSWORD = 'your email_password'
# 사전에 stmp 연동 필요
```

2. url 변경
accounts_app/templates/accounts/signup_email.html
이메일 인증 후 리다이렉트 주소 개인에 맞게 변경
(ex. http://127.0.0.0:8000)
