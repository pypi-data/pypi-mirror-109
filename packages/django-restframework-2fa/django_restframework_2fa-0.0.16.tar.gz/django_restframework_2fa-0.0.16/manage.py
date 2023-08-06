import sys
import os

urlpatterns = []  
# since django will search for ROOT_URLCONF from settings,
# and we have given this same file as ROOT_URLCONF on settings, see below
if __name__ == "__main__":
    import django
    from django.conf import settings
    from django.core.management import execute_from_command_line
    import datetime

    settings.configure(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DEBUG=True,
        ROOT_URLCONF='django_restframework_2fa.urls',
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'django_restframework_2fa'
        ],
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        STATIC_URL = '/static/',
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
        ],

        DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField',

        REST_FRAMEWORK = {
            'DEFAULT_A,UTHENTICATION_CLASSES': (
                'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
            ),
            'TEST_REQUEST_DEFAULT_FORMAT': 'json'
        },

        # set auth model for the application.
        AUTH_USER_MODEL = 'django_restframework_2fa.TestUser',

        SIMPLE_JWT = {
            'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=30),
            'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
        },

        TWILIO_SID = os.environ.get('TWILIO_SID'),
        TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN'),
        TWILIO_SERVICE_ID = os.environ.get('TWILIO_SERVICE_ID'),

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        }
    )
    # Note: you may need to configure database also
    django.setup()  # setup django after configuring settings

    execute_from_command_line(sys.argv)  # let this handle commands as always
