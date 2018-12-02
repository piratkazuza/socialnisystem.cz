"""
Django settings for socialsystem project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import dsnparse
import os
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', '0') is '1'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "no-secret-key"
    else:
        raise RuntimeError("Missing SECRET_KEY environment variable.")


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',

    'django.forms',

    'webpack_loader',
    'markdownx', # A markdown editor
    'markdown_deux', # Markdown rendering template tags
    'capture_tag', # Re-use same block multiple times

    'socialsystem.core.apps.CoreConfig',
    'socialsystem.pages',
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'socialsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'socialsystem', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'socialsystem.context_processors.global_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'socialsystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASE_DSN = os.environ.get("DATABASE_DSN", "postgresql://localhost:5432/socialsystem")
db = dsnparse.parse(DATABASE_DSN)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db.paths[0],
        "USER": db.username,
        "PASSWORD": db.password,
        "HOST": db.host,
        "PORT": db.port,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'cs'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

# Logging
LOGGING = {
    "version": 1,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO" if DEBUG else "WARNING"}
    },
}

# Site
SITE_ID = 1

# HTML minify
HTML_MINIFY = os.environ.get('MINIFY_HTML', DEBUG)

# Custom settings
# ---------------

SITEINFO = {
    'name': 'SocialniSystem.cz',
    'claim': 'pomocník pro vaši orientaci v džungli sociálního systému',
    'description': '',
    'keywords': (),
    'phone': '+420776278860',
    'email': 'info@socialnisystem.cz',
    'fb_profile_url': 'https://facebook.com',
    'twitter_profile_url': 'https://twitter.com',
    'instagram_profile_url': 'https://instagram.com',
    'benefit_calculator_url': 'https://www.pracevobci.cz/kalkulacka/',
    # 'piwik_siteid': '',
}

FOOTER_MENU = (
    {
        'class': 'small-12 medium-4 columns',
        'title': 'Další informace',
        'items': (
            ('internal', 'core:benefit-overview', 'Orientační přehled dávek'),
            ('external', '', 'Výpočet životního minima'),
            ('external', '', 'Rizikové skupiny'),
            ('external', '', 'Zdroje'),
        )
    },
    {
        'class': 'small-12 medium-4 columns',
        'title': 'Nástroje',
        'items': (
            ('external', SITEINFO['benefit_calculator_url'], 'Kalkulačka sociálních dávek'),
            ('external', 'https://portal.mpsv.cz/', 'Integrovaný portál MPSV'),
        )
    },
)


# Webpack-built assets

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/', # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map'],
    }
}

# Markdown
MARKDOWNX_MARKDOWNIFY_FUNCTION = 'socialsystem.markdown.markdownify'

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            "tables": None,
            "header-ids": None,
            "footnotes": None,
        },
        "safe_mode": False,
    },
    # "trusted": {
    #     "safe_mode": False,
    #     "extras": {
    #         "tables": None,
    #         "header-ids": None,
    #         "footnotes": None,
    #     },
    # },
    "target_blank": {
        "extras": {
            "target-blank-links": None,
        },
    }
}
