from django.conf import settings

import requests
from social_core.exceptions import AuthForbidden


def refuse_reassociation(backend, is_new, user, *args, **kwargs):
    if not is_new and user is not None:
        raise AuthForbidden(backend, 'Cannot associate second EVE account.')


def get_character_id(backend, uid, *args, **kwargs):
    return {'character_id': uid}


def refuse_alliance_id(backend, uid, *args, **kwargs):
    if settings.VALID_ALLIANCE_IDS is None:
        return

    data = requests.get('https://esi.tech.ccp.is/latest/characters/%d/?datasource=tranquility' % uid).json()

    if data.get('alliance_id', -1) not in settings.VALID_ALLIANCE_IDS:
        raise AuthForbidden(backend, 'Forbidden alliance ID.')
