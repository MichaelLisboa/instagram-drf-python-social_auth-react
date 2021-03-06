import json
import os
from social_core.backends import instagram

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'accounts',
    'memberships',

    # 3rd party
    'rest_framework',
    'social_django',
    'oauth2_provider',
    'rest_framework_social_oauth2',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True

instagram.InstagramOAuth2.REDIRECT_STATE = False
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_INSTAGRAM_KEY = os.environ.get('IG_ID')
SOCIAL_AUTH_INSTAGRAM_SECRET = os.environ.get('IG_SECRET')

SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'

SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope': 'basic public_content'}

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.auth_allowed',
    'backend.pipeline.create_user',
    'backend.pipeline.link_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    # 'backend.pipeline.create_subscription',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social_core.pipeline.disconnect.allowed_to_disconnect',
    'social_core.pipeline.disconnect.get_entries',
    'social_core.pipeline.disconnect.revoke_tokens',
    'social_core.pipeline.disconnect.disconnect',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.LimitOffsetPagination'
    ),
    'PAGE_SIZE': 25,
    'DEFAULT_METADATA_CLASS': (
        'rest_framework.metadata.SimpleMetadata'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '1000/day'
    # }
}

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'social_core.backends.instagram.InstagramOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'PORT': '5432',
        'CONN_MAX_AGE': 60 * 10,
    }
}

HOST_URL = 'https://influense-rs-dot-pixt-app-1.appspot.com/'

if os.getenv('GAE_INSTANCE'):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASES['default']['HOST'] = os.environ.get('DB_HOST')
    DATABASES['default']['NAME'] = os.environ.get('DB_NAME')
    DATABASES['default']['USER'] = os.environ.get('DB_USER')
    DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASS')

    EMAIL_HOST = os.environ['email_host']
    EMAIL_HOST_USER = os.environ['email_user']
    DEFAULT_FROM_EMAIL = os.environ['email_user']
    SERVER_EMAIL = os.environ['email_user']
    EMAIL_HOST_PASSWORD = os.environ['email_pass']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    STATIC_URL = os.environ.get('BUCKET')
    STATIC_ROOT = 'static/'
else:
    with open('bin/connections.json') as f:
        data = json.load(f)

    SECRET_KEY = data['secret_key']

    DEBUG = True
    HOST_URL = 'http://127.0.0.1:8000/'

    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['NAME'] = data['db_name']
    DATABASES['default']['USER'] = data['db_user']
    DATABASES['default']['PASSWORD'] = data['db_pass']

    EMAIL_HOST = data['email_host']
    EMAIL_HOST_USER = data['email_user']
    DEFAULT_FROM_EMAIL = data['email_user']
    SERVER_EMAIL = data['email_user']
    EMAIL_HOST_PASSWORD = data['email_pass']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    CORS_ORIGIN_ALLOW_ALL = True
