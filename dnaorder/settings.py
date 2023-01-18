"""
Django settings for dnaorder project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default='127.0.0.1').split()

SITE_ID = int(os.environ.get("SITE_ID", default=1))

MULTI_SITE = int(os.environ.get("MULTI_SITE", default=0))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
#     'rest_framework_filters',
    'django_filters',
#     'material',
    'dnaorder',
    'billing',
    'corsheaders',
    'social_django'
#     'django_mailbox'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionMiddleware',
    
#     'django.contrib.auth.middleware.PersistentRemoteUserMiddleware',
#     'dnaorder.middleware.OIDCMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.keycloak.KeycloakOAuth2',
    # 'social_core.backends.google.GoogleOpenId',
    # 'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.twitter.TwitterOAuth',
    # 'social_core.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
)
# AUTHENTICATION_BACKENDS = [
# #     'django.contrib.auth.backends.RemoteUserBackend',
#     'django.contrib.auth.backends.ModelBackend'
# ]

ROOT_URLCONF = 'dnaorder.urls'

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
                'django.template.context_processors.media',
                'dnaorder.context_processors.url_processor',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'dnaorder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SQL_DATABASE", "postgres"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
FILES_ROOT = os.environ.get("FILES_ROOT", default=BASE_DIR) #let another path outside app folder be used, such as "/data" so you can mount a network filesystem
STATIC_ROOT = os.path.join(FILES_ROOT,'static')
MEDIA_ROOT = os.path.join(FILES_ROOT,'media')

SENDFILE_BACKEND = 'sendfile.backends.simple'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny'
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter',
                                'rest_framework.filters.SearchFilter'],
#     ('rest_framework_filters.backends.DjangoFilterBackend','rest_framework.filters.OrderingFilter', 'rest_framework.filters.SearchFilter'),
    'DEFAULT_PAGINATION_CLASS': 'dnaorder.api.pagination.StandardPagePagination',
    'PAGE_SIZE': 10,
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 10000,
    'EXCEPTION_HANDLER': 'dnaorder.api.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ]
}

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", default='django.core.mail.backends.console.EmailBackend')#'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST", default='')
EMAIL_USE_TLS = True
EMAIL_PORT = 587


BASE_URI = os.environ.get("BASE_URI", default='http://127.0.0.1')

LAB_EMAIL = os.environ.get("LAB_EMAIL", default='example@coreomics.com')

PAYMENT_TYPES = [] # ['dnaorder.payment.ppms.serializers.PPMSPaymentType']

PLUGINS = os.environ.get("PLUGINS", default="").split()
PLUGIN_APPS = os.environ.get("PLUGIN_APPS", default="").split()


from corsheaders.defaults import default_headers
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = default_headers + tuple(os.environ.get("CORS_ALLOW_HEADERS", default='X-XSRF-TOKEN').split())
CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", default="http://127.0.0.1").split()
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", default="http://127.0.0.1").split()

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True

FORCE_SCRIPT_NAME = '/server' # prepend to base urls

# if not os.environ.get("SECRET_KEY"):
#     from dnaorder.local_config import *
# else:
#     from dnaorder.config import *

#shouldn't need this in default settings
PPMS_URL = 'https://ppms.us/ucdavis-test/pumapi/'
PPMS_AUTH_TOKEN = 'token'

SOCIAL_AUTH_JSONFIELD_ENABLED = True

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_KEYCLOAK_KEY = os.environ.get("SOCIAL_AUTH_KEYCLOAK_KEY", default='client_id')
SOCIAL_AUTH_KEYCLOAK_SECRET = os.environ.get("SOCIAL_AUTH_KEYCLOAK_SECRET", default='')
SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = os.environ.get("SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY", default='')
SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = os.environ.get("SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL", default='') # 'https://foo.com/auth/realms/submissions/protocol/openid-connect/auth'
SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = os.environ.get("SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL", default='') # 'https://foo.com/auth/realms/submissions/protocol/openid-connect/token'

SOCIAL_AUTH_LOGIN_URL = '/server/login/'


SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. In some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social_core.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social_core.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',
)

SOCIAL_LOGIN_URL = os.environ.get("SOCIAL_LOGIN_URL", default='/server/social/login/keycloak/')

try:
    from dnaorder.config import *
except:
    print('no config file')

# raise Exception(PLUGIN_APPS)
INSTALLED_APPS += PLUGIN_APPS
# for PLUGIN in PLUGINS:
#     INSTALLED_APPS.append(PLUGIN)

# from plugins import PluginManager

# PLUGIN_MANAGER = PluginManager(PLUGINS=PLUGINS)
# for app in PLUGIN_MANAGER.apps:
#     INSTALLED_APPS.append(app)