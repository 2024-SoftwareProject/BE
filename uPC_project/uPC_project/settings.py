"""
Django settings for uPC_project project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import private_settings
DATABASES = private_settings.DATABASES
SECRET_KEY = private_settings.SECRET_KEY


from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # pip install django-bootstrap5
    'django_bootstrap5',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # provider
    'allauth.socialaccount.providers.kakao',

    # app
    'accounts_app',
    'uPC_app',
    'products_app',
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'uPC_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uPC_project.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 디폴트 SITE의 id / 등록을 하지 않으면, 각 요청 시에 host명의 Site 인스턴스를 찾는다 .
SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# email 설정
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'upc_sw1004@naver.com'
EMAIL_HOST_PASSWORD = private_settings.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# # [accounts 추가 설정]
# 이거 안 하면 내가 만든 User모델 못 사용함 //  accounts_app/models.py/class User
AUTH_USER_MODEL = 'accounts_app.User'

# 인증 방법은 email 통해 진행/ email 회원가입에 필요
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

# 인증되어야 로그인 가능하도록
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# get 방식으로 email 인증에 접속했을때 허용
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# 바로 카카오 로그인페이지로 이동
SOCIALACCOUNT_LOGIN_ON_GET = True

# 로그아웃 후 리다이렉트할 페이지
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'
# 로그아웃 버튼 클릭 시 자동 로그아웃
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_PASSWORD_RESET_ON_GET = True

# 로그인 후 리다이렉트할 페이지
LOGIN_REDIRECT_URL = 'home'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_URL = 'accounts/login'
LOGOUT_URL = 'accounts/logout'


# session 만료 시간 3시간
SESSION_COOKIE_AGE = 10800