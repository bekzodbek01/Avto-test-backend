"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n1ip$1ezinlr5er4irj9wmx=u@3n4b*v5t-has8525(+w^!*81'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # install app
    'rest_framework',
    'drf_yasg',

    # my app
    'my_users',
    'exams',

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'avto',
#         'USER': 'user_avto',
#         'PASSWORD': 'password_avto',
#         'HOST': 'avto_db',  # Docker Compose'dagi PostgreSQL service nomi
#         'PORT': '5432',
#     }
# }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # ✅ JWT Authentication
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=36500),  # 100 yil
    "REFRESH_TOKEN_LIFETIME": timedelta(days=73000),  # 200 yil
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
STATIC_URL = '/static/'

# Agar logo faylingiz `static/` papkasida bo'lsa
STATICFILES_DIRS = [
    BASE_DIR / "static", ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media fayllar uchun katalog
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

JAZZMIN_SETTINGS = {
    # "site_title": "Foydali Havolalar",
    "site_brand": "Avto test",
    "site_title": "Avto Test Admin",
    "site_header": "Avto Test Boshqaruvi",
    "site_logo": "avto.jpg",
    "welcome_sign": "Avto Test tizimiga xush kelibsiz!",
    "copyright": "Avto Test",
    # "search_model": ["app.model_name"],

    "topmenu_links": [
        {"model": "auth.User"},
        # {"model": "auth.Group"},

        # {"name": "Foydali Havolalar", "url": "foydali_havolalar"},
        # {"name": "Hikmatli Sozlar", "url": "hikmatli_sozlar"},
        # {"name": "Hujjatlar", "url": "hujjatlar"},
        # {"name": "Ishtirokchilar", "url": "ishtirokchilar"},
        # {"name": "Jadidlar", "url": "jadidlar"},
        # {"name": "Manbalar", "url": "manbalar"},
        # {"name": "Sahifalar", "url": "sahifalar"},
        # {"name": "Slayder", "url": "slayder"},
        # {"name": "Tadbirlar", "url": "tadbirlar"},
        # {"name": "Tanlovlar", "url": "tanlovlar"},
    ],

    "navigation_expanded": False,

    "hide_apps": ['auth'],

    "show_ui_builder": True,

    "changeform_format": "collapsible",

    # "usermenu_links": [
    # {"name": "Profile", "url": "profile"},
    # {"name": "Logout", "url": "logout"},
    # {"name": "Login", "url": "login"},
    # {"name": "Signup", "url": "signup"},

    #     ]

}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 209715200  # 200 MB (baytlarda)
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200  # 200 MB

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
