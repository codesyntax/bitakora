from django.conf import settings
from photologue.models import Photo
from django.contrib.sites.shortcuts import get_current_site

BITAKORA_CUSTOM_LOGO = getattr(settings, 'BITAKORA_CUSTOM_LOGO', '')
BITAKORA_CUSTOM_CSS = getattr(settings, 'BITAKORA_CUSTOM_CSS', '')
BITAKORA_CUSTOM_MINILOGO = getattr(settings, 'BITAKORA_CUSTOM_MINILOGO', '')
BITAKORA_CUSTOM_FAVICON = getattr(settings, 'BITAKORA_CUSTOM_FAVICON', '')
PROFILE_PHOTO_DEFAULT = getattr(settings, 'PROFILE_PHOTO_DEFAULT', '')

def bitakora_custom(request):
    try:
        photo = Photo.objects.get(slug=PROFILE_PHOTO_DEFAULT)
    except:
        photo = None
    return {
        'CUSTOM_FAVICON': BITAKORA_CUSTOM_FAVICON,
        'CUSTOM_LOGO': BITAKORA_CUSTOM_LOGO,
        'CUSTOM_MINILOGO': BITAKORA_CUSTOM_MINILOGO,
        'CUSTOM_CSS': BITAKORA_CUSTOM_CSS,
        'PROFILE_PHOTO_DEFAULT': photo,
        'HOST': get_current_site(request),
    }