from photologue.models import Photo
from bitakora.photologue_custom.models import PhotoExtended
from django.template.defaultfilters import slugify
from slug import time_slug_string

def handle_uploaded_file(f,author):
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