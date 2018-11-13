"""
Django settings for my_website_api project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#_e7pguwap-q*setp+m#4+whhzfjl@od6ewt=5)h-f!^j!k94%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 跨越问题的解决，允许跨越请求接口的主机
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Application definition
# get 请求url不用加后面的/
APPEND_SLASH = True

INSTALLED_APPS = [
    'django.contrib.admin',  # admin管理后台站点
    'django.contrib.auth',  # 身份认证系统
    'django.contrib.contenttypes',  # 内容类型框架
    'django.contrib.sessions',  # 会话框架
    'django.contrib.messages',  # 消息框架
    'django.contrib.staticfiles',  # 静态文件管理框架
    'api',
    'login',
    'captcha',  # 图形验证码用到的库
    'corsheaders',  # 解决跨域相关的库
    'rest_framework'  # 请求返回相关的库
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  #  允许跨越的设置，他的位置只能放在这里（'django.contrib.sessions.middleware.SessionMiddleware'后面）
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_website_api.urls'
# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '2297820776@qq.com'
EMAIL_HOST_PASSWORD = 'lgbwlgbxgizediab'
DEFAULT_FROM_EMAIL = '2297820776@qq.com'
CONFIRM_DAYS = 1

# 配置前端模块的路径, django搜索模板的时候，会按照以下的配置的搜索路径和引擎进行render模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
    # 可以在这里添加多个模板搜索引擎和搜索路径， 如添加jinja
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
          os.path.join(BASE_DIR, 'templates/jinja2')
        ],
    }
]

WSGI_APPLICATION = 'my_website_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# 数据库的设置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_website',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# 这里配置的是静态资源访问的路径，即在模板中使用静态资源时， 在静态资源路径的前面加载这里配置的路径
STATIC_URL = '/static/'

# 前端vue项目的静态资源的存放的路径
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/static/"),
]

# 上传文件的路径配置， 即上传之后， 存放媒体资源的路径
MEDIA_ROOT = os.path.join(BASE_DIR, "static/images/")
MEDIA_URL = '/upload/'  #访问媒体资源的路径， 即这个是在浏览器上访问该文件的url的前缀