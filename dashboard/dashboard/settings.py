import os
import pymysql
from pathlib import Path

# Then your existing line

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zs#9ry5k4tz30dw#_bqdzg*u-yf#q7bbpfz@7&(joaiz*6sqdh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.0.0.0.0','localhost', '127.0.0.1', '147.139.201.95', 'sentinel.investpro.id']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'message',
    'dast_reports',
    'sast_report',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# settings.py
JENKINS_CONFIG = {
    'BASE_URL': 'http://sentinel.investpro.id:8080',
    'USERNAME': 'admin',
    'API_TOKEN': '11c405e35f3f22adeaa1473199d9bad0c9',
    'ZAP_JOB_NAME': 'DAST-Automasi',
    'ZAP_JOB_TOKEN': 'opsitechsec2020'  # Jika menggunakan trigger token
}

ROOT_URLCONF = 'dashboard.urls'


# Tambah di settings.py
LOGIN_REDIRECT_URL = '/sast-report/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dashboard/templates')], # Tempatkan di sini
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
WSGI_APPLICATION = 'dashboard.wsgi.application'

# settings.py - Tambahkan ini
LOGOUT_REDIRECT_URL = '/login/'  # Redirect setelah logout

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
	'USER': 'root',
	'PASSWORD': 'Infovesta2020#',
	'HOST': 'localhost',
	'port': '3306',
	'OPTIONS': {
            'charset': 'utf8mb4',
    }
  }
}

# DeepSeek API Configuration
OPENROUTER_API_KEY = "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"  # Key OpenRouter Anda
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek/deepseek-chat-v3.1:free"  # Model yang digunakan


#celellry
# settings.py
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# SAST Configuration
SAST_CONFIG = {
    'DOCKER_ENABLED': True,
    'SEMGREP_IMAGE': 'returntocorp/semgrep:latest',
    'SCAN_TIMEOUT': 1800,  # 30 minutes
    'MAX_CONCURRENT_SCANS': 3,
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dashboard/static'),
]



# Email configuration (example for Gmail)
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'your-email@gmail.com'
#EMAIL_HOST_PASSWORD = 'your-app-password'
#DEFAULT_FROM_EMAIL = 'Opsitech Guard <your-email@gmail.com>'
#ADMIN_EMAIL = 'admin@opsitech.com'
#BASE_URL = 'https://yourdomain.com'  # for admin links in emails
#"""


