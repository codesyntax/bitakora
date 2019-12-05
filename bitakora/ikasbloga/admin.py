from .models import School, Level, Room
from django.contrib import admin


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',), }
    search_fields = ['name', ]
    ordering = ('name',)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',), }
    search_fields = ['name', ]
    ordering = ('name',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',), }
    search_fields = ['name', ]
    ordering = ('name',)

admin.site.register(School, SchoolAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Room, RoomAdmin)