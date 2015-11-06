from django.conf.urls import patterns, url, include

urlpatterns = patterns('bitakora.base.views',
    (r'^$','index'),
)
