from models import *
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



class BlogAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name',]
    ordering = ('name',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','slug','blog')
    list_display_links = ('title',)
    search_fields = ['title',]
    ordering = ('title',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Article,ArticleAdmin)