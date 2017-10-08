# TODO: Copy this file to 'local.py' and fill in values.

import os

from elmo.settings.base import *

SECRET_KEY = 'YOUR KEY GOES HERE'
DEBUG = True
ALLOWED_HOSTS = []

SOCIAL_AUTH_EVEONLINE_KEY = ''
SOCIAL_AUTH_EVEONLINE_SECRET = ''
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

# None if all alliances can access this app, otherwise a list of ID's.
VALID_ALLIANCE_IDS = None

MOON_TRACKER_MINIMUM_SCANS = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
