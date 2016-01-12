from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bitakora.views import DataGetCategories
from bitakora.base.models import Article
from voting.views import vote_on_object
from django.contrib.flatpages import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

article_dict = {
    'model': Article,
    'template_object_name': 'article',
}


urlpatterns = patterns('',
    #Uncomment the line below and put the correct project name
    (r'^$','bitakora.views.index'),
    url(r'^category/(?P<slug>[\-\d\w]+)$','bitakora.views.category', name='category'),
    url(r'^top_stories$', 'bitakora.views.top_stories', name='top_stories'),
    url(r'^bookmarks$', 'bitakora.views.bookmarks', name='bookmarks'),
    url(r'^users$','django.contrib.auth.views.login', name='erabiltzailea_user_login'),
    url(r'^users/useroptions$','bitakora.views.useroptions', name='useroptions'),
    url(r'^users/edit-profile$','bitakora.accounts.views.edit_profile', name='edit_profile'),
    url(r'^users/edit-blog$','bitakora.accounts.views.edit_blog', name='edit_blog'),
    url(r'^users/edit-pass$','bitakora.accounts.views.edit_pass', name='edit_pass'),
    (r'^/users/accounts$', include('registration.backends.default.urls')),
    (r'^users/', include('cssocialuser.urls')),

    url(r'^voting/(?P<object_id>\d+)/(?P<direction>up|down|clear)?$', vote_on_object, article_dict, name="vote_on_object"),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^ajax/get_categories$', DataGetCategories.as_view(), name='get_categories'),

    (r'^tinymce/', include('tinymce.urls')),

    (r'^search/', include('haystack.urls')),

    url(r'^learn-more/$', views.flatpage, {'url': '/learn-more/'}, name='learn-more'),

    url(r'^ajax/categories/', 'bitakora.views.get_categories', name='ajax_categories'),
    url(r'^ajax/related_posts/', 'bitakora.views.get_related_posts', name='ajax_related_posts'),

    (r'^', include('bitakora.base.urls')),
)

urlpatterns += staticfiles_urlpatterns()