import os
from flask_appbuilder.security.manager import AUTH_OID, \
                                          AUTH_REMOTE_USER, \
                                          AUTH_DB, AUTH_LDAP, \
                                          AUTH_OAUTH
if os.getenv('IS_ECS'):
    import urllib.request
    HOST_IP = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/local-ipv4').read()

META_DB_URL = os.getenv('META_DB_URL', '')
META_DB_USER = os.getenv('META_DB_USER', '')
META_DB_PASSWORD = os.getenv('META_DB_PASSWORD', '')
SQLALCHEMY_DATABASE_URI = META_DB_URL.format(META_DB_USER=META_DB_USER, META_DB_PASSWORD=META_DB_PASSWORD)

AUTH_TYPE = AUTH_DB
OAUTH_PROVIDERS = [
    {'name':'google', 'icon':'fa-google', 'token_key':'access_token',
        'whitelist': ['@zomato.com'],
        'remote_app': {
            'base_url':'https://www.googleapis.com/oauth2/v2/',
            'request_token_params':{
              'scope': 'email profile'
            },
            'consumer_key':os.getenv('GOOGLE_LOGIN_KEY'),
            'consumer_secret':os.getenv('GOOGLE_LOGIN_SECRET'),
            'request_token_url':None,
            'access_token_url':'https://accounts.google.com/o/oauth2/token',
            'authorize_url':'https://accounts.google.com/o/oauth2/auth'
        }
    }
]

AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = os.getenv('AUTH_USER_REGISTRATION_ROLE', 'Gamma')

ROW_LIMIT = os.getenv('ROW_LIMIT')
if ROW_LIMIT:
    ROW_LIMIT = int(ROW_LIMIT)
else:
    ROW_LIMIT = 5000

SQL_MAX_ROW = os.getenv('SQL_MAX_ROW')
if SQL_MAX_ROW:
    SQL_MAX_ROW = int(SQL_MAX_ROW)
else:
    SQL_MAX_ROW = 10000

SECRET_KEY = '\2\1woahthisismysecretkey\1\2\e\y\y\h'

REDIS_URL_FOR_CACHE = os.getenv('REDIS_URL_FOR_CACHE', '')
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24, # 1 day default (in secs)
    'CACHE_KEY_PREFIX': 'superset_cached',
    'CACHE_REDIS_URL': REDIS_URL_FOR_CACHE,
}

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
class CeleryConfig(object):
    BROKER_URL = CELERY_BROKER_URL
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    
CELERY_CONFIG = CeleryConfig

if os.getenv('RESULT_BACKEND_S3_CACHE_BUCKET'):
    from s3cache.s3cache import S3Cache
    S3_CACHE_BUCKET = os.getenv('RESULT_BACKEND_S3_CACHE_BUCKET', '')
    S3_CACHE_KEY_PREFIX = 'superset_results'
    RESULTS_BACKEND = S3Cache(S3_CACHE_BUCKET, S3_CACHE_KEY_PREFIX)
else:
    RESULT_BACKEND_REDIS_HOST = os.getenv('RESULT_BACKEND_REDIS_HOST', '')
    from werkzeug.contrib.cache import RedisCache
    RESULTS_BACKEND = RedisCache(
        host=RESULT_BACKEND_REDIS_HOST, port =6379, key_prefix='superset_results')

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

if os.getenv('SUPERSET_STATSD_ENABLE') == 'True':
    SUPERSET_STATSD_HOST = os.getenv('SUPERSET_STATSD_HOST')
    if not SUPERSET_STATSD_HOST and os.getenv('IS_ECS'):
        SUPERSET_STATSD_HOST = HOST_IP
    if SUPERSET_STATSD_HOST:
        from superset.stats_logger import StatsdStatsLogger
        STATS_LOGGER = StatsdStatsLogger(host=SUPERSET_STATSD_HOST, port=8125, prefix='superset')
