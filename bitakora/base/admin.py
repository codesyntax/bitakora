from models import *
from forms import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class BlogAdmin(admin.ModelAdmin):
    def admin_thumbnail(self,obj):
        if obj.header_image:
            return obj.header_image.admin_thumbnail()
        return ''
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True


    list_display = ('name','user','template','admin_thumbnail')
    list_display_links = ('name',)
    radio_fields = {"template": admin.HORIZONTAL}
    search_fields = ['name',]
    ordering = ('name',)

class ArticleAdmin(admin.ModelAdmin):

    def admin_thumbnail(self,obj):
        if obj.featured_image:
            return obj.featured_image.admin_thumbnail()
        return ''
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    list_display = ('title','slug','blog','status','publish_date','expiry_date','admin_thumbnail')
    list_display_links = ('title',)
    
    list_filter = ("status",)
    list_editable = ("status",)
    radio_fields = {"status": admin.HORIZONTAL}
    prepopulated_fields = {'slug':('title',)} 
    raw_id_fields = ('blog','featured_image',"related_posts",'categories')
    search_fields = ['title',]
    ordering = ('-publish_date',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','nickname','email','parent','text','publish_date','status')
    list_display_links = ('user','user')
    search_fields = ['user__username', 'nickname','text']
    list_editable = ("status",)
    radio_fields = {"status": admin.HORIZONTAL}
    ordering = ('-publish_date',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','slug')
    list_display_links = ('title',)
    prepopulated_fields = {'slug':('title',)} 
    search_fields = ['title',]
    ordering = ('title',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)