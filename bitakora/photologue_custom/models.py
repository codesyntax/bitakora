# -*- coding: utf-8 -*-

from django.db import models
from photologue.models import Photo
from bitakora.utils.models import get_user_model_name
from django.utils.translation import ugettext_lazy as _

user_model_name = get_user_model_name()

class PhotoExtended(models.Model):

    # Link back to Photologue's Photo model.
    photo = models.OneToOneField(Photo, related_name='extended')

    author = models.ForeignKey(user_model_name, verbose_name=_("Author"),
        related_name="%(class)ss")

    class Meta:
        verbose_name = u'Extra fields'
        verbose_name_plural = u'Extra fields'

    def __str__(self):
        return self.photo.title