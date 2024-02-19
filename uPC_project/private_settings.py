# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'upc_db', # mydatabase
        'USER': 'dlfroal', # mydatabaseuser
        'PASSWORD': 'thdnp22', # mypassword
        'HOST': '10.28.1.16', # host
        'PORT': '3306',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1!+o277jmi28p27u0-i3ay_w++)+!lft)3t*(*f9s0%6i=d_k^'

# Email smtp
EMAI_HOST_PASSWORD = 'thdnp@1004'