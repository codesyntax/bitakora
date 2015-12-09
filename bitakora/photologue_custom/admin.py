# -*- coding: utf-8 -*-

from django.contrib import admin

from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.models import Photo
from .models import PhotoExtended


class PhotoExtendedInline(admin.StackedInline):
    model = PhotoExtended
    can_delete = False


class PhotoAdmin(PhotoAdminDefault):

    def admin_thumbnail(self,obj):
        if obj:
            return u'<img src="%s" />' % (obj.get_admin_thumbnail_url())
        else:
            return u'(Irudirik ez)'
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True


    def author(self,obj):
        try: 
            return obj.extended.author or ""
        except:
            return ""


    list_display = ('title','author','date_taken','date_added','is_public','admin_thumbnail')
    list_display_links = ('title',)
    search_fields = ['title','caption']

    inlines = [PhotoExtendedInline, ]

admin.site.unregister(Photo)
admin.site.register(Photo, PhotoAdmin)