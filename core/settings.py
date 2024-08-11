
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "django_htmx",
    "accounts.apps.AccountsConfig",
    "vendor.apps.VendorConfig",
    "menu.apps.MenuConfig",
    "marketplace.apps.MarketplaceConfig",
    "customer.apps.CustomerConfig",
    "orders.apps.OrdersConfig",
    "tailwind",
    "theme",
    "django_browser_reload",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    'accounts.middlewares.CrossOriginOpenerPolicyMiddleware',
    "orders.middleware.RequestObject",
    "django_browser_reload.middleware.BrowserReloadMiddleware",

]
ROOT_URLCONF = "core.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processorss.get_vendor",
                "accounts.context_processorss.get_user_profile",
                "accounts.context_processorss.get_paypal_client_id",
                "marketplace.context_processors.get_cart_counter",
                "marketplace.context_processors.get_cart_amounts",
            ],
        },
    },
]
WSGI_APPLICATION = "core.wsgi.application"
TAILWIND_APP_NAME = "theme"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / 'db.sqlite3',
        # "USER":config('USER'),
        # "PASSWORD":config('PASSWORD'),
        # "HOST":config('HOST')
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = ["core/static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Email configuration settings
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT',cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')

# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')



AUTH_USER_MODEL = "accounts.User"
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "blue",
    messages.INFO: "blue",
    messages.SUCCESS: "green",
    messages.WARNING: "yellow",
    messages.ERROR: "red",
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')


# EMAIL_USE_TLS = True  # For Gmail, use TLS; for other providers, adjust accordingly
# EMAIL_HOST_USER = 'your_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_password'
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    # for apply every where pagination

    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.TokenAuthentication',
    # ),s
}