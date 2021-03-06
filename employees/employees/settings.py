"""
Django settings for employees project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*#9z!5s9jsceia1d69g1&+@evqb$##_1w%%u!v=wqc4&&j1vj6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
ALLOWED_HOSTS = [".127.0.0.1",".localhost"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'employeeapp',

   )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
 
)

ROOT_URLCONF = 'employees.urls'

WSGI_APPLICATION = 'employees.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


path=os.path.abspath("..")


MEDIA_ROOT=path + "/employees/static/static/img/uploads"

MEDIA_URL="http://localhost:8000/static/static/img/uploads/"


IMAGE_ROOT=path + "/employees/static/static/img/uploads/"


# # Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/





LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_USE_TLS = True 
EMAIL_HOST='smtp.anipr.in'

EMAIL_PORT = '587'

# CONFIRM_MOBILE = '08978028038' 

# EMAIL_HOST_USER = 'venugopal@anipr.in'
# EMAIL_HOST_PASSWORD = '8885662223chinna'

EMAIL_HOST_USER = 'avishek@anipr.in'
EMAIL_HOST_PASSWORD = 'iitaieee2012'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/




STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR,"static/")

TEMPLATE_DIRS=(
    os.path.join(BASE_DIR,"static","templates"),
    )


STATICFILES_DIRS=(
    os.path.join(BASE_DIR,"static","static"),

    )
