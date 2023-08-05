from modoboa_automua.frontend.settings import *  # noqa

SECRET_KEY = 'ho^dtq*n7ew+nf-+b)ufru*9rt5)+-iq@d@o$kt_rbn$k26li7'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'default.db',
    },
}
