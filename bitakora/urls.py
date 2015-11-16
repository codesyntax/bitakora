from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    #Uncomment the line below and put the correct project name
    (r'^$','bitakora.views.index'),

    url(r'^users$','django.contrib.auth.views.login', name='erabiltzailea_user_login'),
    (r'^users/', include('cssocialuser.urls')),

    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()