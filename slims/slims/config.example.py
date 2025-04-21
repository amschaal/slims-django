COREOMICS_BASE_URL = 'https://subdomainexample.coreomics.com'
COREOMICS_TOKEN = 'COREOMICS_TOKEN_HERE'

BIOSHARE_USER = 'user@email.edu'
BIOSHARE_TOKEN = 'BIOSHARE_TOKEN_HERE'
BIOSHARE_BASE_URL = 'https://bioshare.domain.com'
BIOSHARE_FILESYSTEM_ID = 1 #fill in default filesystem ID to use
BIOSHARE_DEFAULT_GROUP = None

RUN_TYPE_OPTIONS = {
    # 'Illumina': {
    #     'data_directory_templates': [{'data_path': '/tmp/{run.run_dir}/{lane.lane_dir}', 'repository_subpath': '{run.run_dir}/{lane.lane_dir}'}]
    # }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME":  "slims",
        "USER":  "slims",
        "PASSWORD": 'MYSQL_PASSWORD_HERE',
        "HOST": "127.0.0.1",
        "PORT": "3306",
        # "OPTIONS": {
        #     "charset": 'latin1'
        # }
    }
}

ALLOWED_HOSTS = ['slims.domain.com']

STATIC_ROOT = '/var/www/slims/static'
DEBUG = False
SECRET_KEY = 'SECRET_KEY_HERE'