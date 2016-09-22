from models import Blog, Article, Category, Comment, External_link
from forms import ArticleAdminForm
from django.contrib import admin


class BlogAdmin(admin.ModelAdmin):
    def admin_thumbnail(self, obj):
        if obj.header_image:
            return obj.header_image.admin_thumbnail()
        return ''
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    list_display = ('name', 'user', 'template', 'admin_thumbnail')
    list_display_links = ('name',)
    radio_fields = {"template": admin.HORIZONTAL}
    search_fields = ['name', ]
    raw_id_fields = ('user',)
    ordering = ('name',)


class ArticleAdmin(admin.ModelAdmin):

    def admin_thumbnail(self, obj):
        if obj.featured_image:
            return obj.featured_image.admin_thumbnail()
        return ''
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    form = ArticleAdminForm
    list_display = ('title', 'slug', 'blog', 'status', 'publish_date', 'expiry_date', 'shared', 'admin_thumbnail')
    list_display_links = ('title',)

    list_filter = ("status",)
    list_editable = ("status",)
    radio_fields = {"status": admin.HORIZONTAL}
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('blog', 'featured_image', "related_posts", 'categories')
    search_fields = ['title', ]
    ordering = ('-publish_date',)

    fieldsets = (
        ('Basic data', {
            'fields': ('title', 'slug', 'text', 'featured_image', 'categories', 'blog')
        }),
        ('Publication data', {
            'fields': ('publish_date', 'expiry_date', 'status')
        }),
        ('Extra data', {
            'fields': ('related_posts', 'allow_comments', 'shared')
        })
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'email', 'parent', 'text', 'publish_date', 'status')
    list_display_links = ('user', 'user')
    search_fields = ['user__username', 'nickname', 'text']
    list_editable = ("status",)
    radio_fields = {"status": admin.HORIZONTAL}
    ordering = ('-publish_date',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'slug']
    ordering = ('title',)


class External_linkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'blog')
    list_display_links = ('title',)
    search_fields = ['title', 'url']
    ordering = ('title',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(External_link, External_linkAdmin)
