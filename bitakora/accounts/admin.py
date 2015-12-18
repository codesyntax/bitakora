from django.contrib import admin
from django.utils.translation import ugettext as _
from models import BitakoraUser

class BitakoraUserAdmin(admin.ModelAdmin):
    def admin_thumbnail(self,obj):
        if obj.photo:
            return obj.photo.admin_thumbnail()
        return ''
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True


    def get_email(self, obj):
        """ """
        return obj.email

    def fullname(self, obj):
        """ """
        return obj.get_fullname()

    list_display = ('fullname', 'username','get_email', 'date_joined','is_active', 'is_staff','admin_thumbnail')
    list_display_links = ('fullname','username')
    ordering = ('-date_joined',)
    search_fields = ['email','username',]
    raw_id_fields = ('photo',)


    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        (_('Personal data'),
        {'fields':('fullname', 'email', 'phone', 'photo')},),
        (_('Biography'),
        {'fields': ('bio',)}),
        (_('Social networks'), {
            'fields': ('twitter_id', 'facebook_id', 'openid_id', 'googleplus_id')
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions','last_login'),
                            'classes': ['collapse',],}),
    )

admin.site.register(BitakoraUser, BitakoraUserAdmin)