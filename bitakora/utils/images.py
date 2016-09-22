from photologue.models import Photo
from django.conf import settings
from bitakora.photologue_custom.models import PhotoExtended
from django.template.defaultfilters import slugify
from slug import time_slug_string
from django.core.files.base import ContentFile
import urllib2


def handle_uploaded_file(f, author):
    photo = Photo()
    extra = PhotoExtended()
    photo.title = u'%s %s' % (author, time_slug_string())
    photo.slug = u'%s-%s' % (author, slugify(time_slug_string()))
    photo.image = f
    photo.save()
    extra.photo = photo
    extra.author = author
    extra.save()
    return photo


def handle_url_file(url, author):
    photo = Photo()
    extra = PhotoExtended()
    photo.title = u'%s %s' % (author, time_slug_string())
    photo.slug = u'%s-%s' % (slugify(author), slugify(time_slug_string()))

    img_name = photo.slug + url[url.rfind("."):]
    photo.image.save(img_name, ContentFile(urllib2.urlopen(url).read()))
    photo.save()
    extra.photo = photo
    extra.author = author
    extra.save()
    return photo


def get_pattern(user, num=None):
    if not num:
        num = user.id
    rnum = round(num / 2) % 10

    if rnum in range(0, 4):
        return int(rnum)
    else:
        return get_pattern(user, num=rnum)
