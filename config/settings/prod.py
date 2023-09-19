#import environ

from .base import *

ALLOWED_HOSTS = ['3.37.160.247', 'accountant-sj.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = True

#env = environ.Env()
#environ.Env.read_env(BASE_DIR / '.env')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': '[%CuGC-tBcSO_Feu0w-ylEYU,C3O_E~F',
        'HOST': 'ls-098102bdad1059ed829b930e0c328a97b7e6e7fc.chjohhhovqpj.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}
